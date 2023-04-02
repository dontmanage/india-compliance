dontmanage.ui.form.on("Sales Invoice", {
    refresh(frm) {
        if (!is_e_invoice_applicable(frm)) return;

        if (
            !frm.doc.irn &&
            dontmanage.perm.has_perm(frm.doctype, 0, "submit", frm.doc.name)
        ) {
            frm.add_custom_button(
                __("Generate"),
                () => {
                    dontmanage.call({
                        method: "india_compliance.gst_india.utils.e_invoice.generate_e_invoice",
                        args: { docname: frm.doc.name },
                        callback: () => frm.refresh(),
                    });
                },
                "e-Invoice"
            );
        }
        if (
            frm.doc.irn &&
            is_irn_cancellable(frm) &&
            dontmanage.perm.has_perm(frm.doctype, 0, "cancel", frm.doc.name)
        ) {
            frm.add_custom_button(
                __("Cancel"),
                () => show_cancel_e_invoice_dialog(frm),
                "e-Invoice"
            );
        }
    },
    async on_submit(frm) {
        if (
            frm.doc.irn ||
            !is_e_invoice_applicable(frm) ||
            !gst_settings.auto_generate_e_invoice
        )
            return;

        dontmanage.show_alert(__("Attempting to generate e-Invoice"));

        await dontmanage.xcall(
            "india_compliance.gst_india.utils.e_invoice.generate_e_invoice",
            {
                docname: frm.doc.name,
                throw: false,
            }
        );
    },
    before_cancel(frm) {
        if (!frm.doc.irn) return;

        dontmanage.validated = false;

        return new Promise(resolve => {
            const continueCancellation = () => {
                dontmanage.validated = true;
                resolve();
            };

            if (!is_irn_cancellable(frm) || !india_compliance.is_e_invoice_enabled()) {
                const d = dontmanage.warn(
                    __("Cannot Cancel IRN"),
                    __(
                        `You should ideally create a <strong>Credit Note</strong>
                        against this invoice instead of cancelling it. If you
                        choose to proceed, you'll be required to manually exclude this
                        IRN when filing GST Returns.<br><br>

                        Are you sure you want to continue?`
                    ),
                    continueCancellation,
                    __("Yes")
                );

                d.set_secondary_action_label(__("No"));
                return;
            }

            return show_cancel_e_invoice_dialog(frm, continueCancellation);
        });
    },
});

function is_irn_cancellable(frm) {
    const e_invoice_info = frm.doc.__onload && frm.doc.__onload.e_invoice_info;
    return (
        e_invoice_info &&
        dontmanage.datetime
            .convert_to_user_tz(e_invoice_info.acknowledged_on, false)
            .add("days", 1)
            .diff() > 0
    );
}

function show_cancel_e_invoice_dialog(frm, callback) {
    const d = new dontmanage.ui.Dialog({
        title: frm.doc.ewaybill
            ? __("Cancel e-Invoice and e-Waybill")
            : __("Cancel e-Invoice"),
        fields: [
            {
                label: "IRN Number",
                fieldname: "irn",
                fieldtype: "Data",
                read_only: 1,
                default: frm.doc.irn,
            },
            {
                label: "e-Waybill Number",
                fieldname: "ewaybill",
                fieldtype: "Data",
                read_only: 1,
                default: frm.doc.ewaybill || "",
            },
            {
                label: "Reason",
                fieldname: "reason",
                fieldtype: "Select",
                reqd: 1,
                default: "Data Entry Mistake",
                options: [
                    "Duplicate",
                    "Data Entry Mistake",
                    "Order Cancelled",
                    "Others",
                ],
            },
            {
                label: "Remark",
                fieldname: "remark",
                fieldtype: "Data",
                reqd: 1,
                mandatory_depends_on: "eval: doc.reason == 'Others'",
            },
        ],
        primary_action_label: frm.doc.ewaybill
            ? __("Cancel IRN & e-Waybill")
            : __("Cancel IRN"),
        primary_action(values) {
            dontmanage.call({
                method: "india_compliance.gst_india.utils.e_invoice.cancel_e_invoice",
                args: {
                    docname: frm.doc.name,
                    values: values,
                },
                callback: function () {
                    frm.refresh();
                    callback && callback();
                },
            });
            d.hide();
        },
    });

    d.show();
}

function is_e_invoice_applicable(frm) {
    return (
        india_compliance.is_e_invoice_enabled() &&
        frm.doc.docstatus == 1 &&
        frm.doc.company_gstin &&
        frm.doc.gst_category != "Unregistered" &&
        !frm.doc.items[0].is_non_gst &&
        moment(frm.doc.posting_date).diff(gst_settings.e_invoice_applicable_from) >= 0
    );
}
