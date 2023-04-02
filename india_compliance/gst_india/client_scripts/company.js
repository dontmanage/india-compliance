{% include "india_compliance/gst_india/client_scripts/party.js" %}

const DOCTYPE = "Company";

validate_pan(DOCTYPE);
validate_gstin(DOCTYPE);
update_gstin_in_other_documents(DOCTYPE);
show_overseas_disabled_warning(DOCTYPE);
set_gstin_query(DOCTYPE);

dontmanage.ui.form.off(DOCTYPE, "make_default_tax_template");
dontmanage.ui.form.on(DOCTYPE, {
    setup(frm) {
        dontmanageerp.company.set_custom_query(frm, [
            "default_customs_expense_account",
            { root_type: "Expense" },
        ]);
        dontmanageerp.company.set_custom_query(frm, [
            "default_customs_payable_account",
            { root_type: "Liability" },
        ]);
    },

    make_default_tax_template: function (frm) {
        if (frm.doc.country !== "India") return;

        dontmanage.call({
            method: "india_compliance.gst_india.overrides.company.make_default_tax_templates",
            args: { company: frm.doc.name },
            callback: function () {
                dontmanage.msgprint(__("Default Tax Templates created"));
            },
        });
    },
});
