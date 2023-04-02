const DOCTYPE = "Delivery Note";
setup_e_waybill_actions(DOCTYPE);

dontmanage.ui.form.on(DOCTYPE, {
    after_save(frm) {
        if (
            frm.doc.docstatus ||
            frm.doc.customer_address ||
            !(gst_settings.enable_e_waybill && gst_settings.enable_e_waybill_from_dn)
        )
            return;

        dontmanage.show_alert({
            message: __("Billing Address is required to create e-Waybill"),
            indicator: "yellow",
        }, 10);
    },
});
