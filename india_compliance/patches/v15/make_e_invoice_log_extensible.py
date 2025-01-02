import dontmanage


def execute():
    e_invoice_log = dontmanage.qb.DocType("e-Invoice Log")

    dontmanage.qb.update(e_invoice_log).set(
        e_invoice_log.reference_name, e_invoice_log.sales_invoice
    ).set(e_invoice_log.reference_doctype, "Sales Invoice").run()
