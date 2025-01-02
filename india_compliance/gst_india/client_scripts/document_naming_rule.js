dontmanage.require("assets/india_compliance/js/transaction.js", function () {
    dontmanage.ui.form.on("Document Naming Rule", {
        async document_type(frm) {
            await show_gst_invoice_no_banner(frm);
        },
    });
});
