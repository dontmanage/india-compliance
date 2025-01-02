import dontmanage


def execute():
    template_name = "e-Invoice QR Code"
    if dontmanage.db.exists(
        "Web Template Field",
        {"parent": template_name, "fieldname": "e_invoice_qr_text"},
    ):
        dontmanage.db.delete("Web Template", template_name)
