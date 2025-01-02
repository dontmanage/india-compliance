import dontmanage
from dontmanage.query_builder.functions import Coalesce
from dontmanage.utils import sbool


def execute():
    # Sales Invoice should have field signed_einvoice
    # and E Invoice Settings should be enabled

    if not dontmanage.db.has_column("Sales Invoice", "signed_einvoice") or not sbool(
        dontmanage.db.get_value(
            "E Invoice Settings", "E Invoice Settings", "enable", ignore=True
        )
    ):
        set_not_applicable_status()
        return

    dontmanage.db.sql(
        """
        UPDATE `tabSales Invoice` SET einvoice_status = 'Pending'
        WHERE
            IFNULL(einvoice_status, '') = ''
            AND posting_date >= '2021-04-01'
            AND docstatus = 1
            AND IFNULL(irn, '') = ''
            AND IFNULL(billing_address_gstin, '') != IFNULL(company_gstin, '')
            AND IFNULL(gst_category, '') in ('Registered Regular', 'SEZ', 'Overseas', 'Deemed Export')
    """
    )

    dontmanage.db.sql(
        """UPDATE `tabSales Invoice` SET einvoice_status = 'Generated'
        WHERE
            IFNULL(einvoice_status, '') = ''
            AND IFNULL(irn, '') != ''
            AND IFNULL(irn_cancelled, 0) = 0"""
    )

    dontmanage.db.sql(
        """UPDATE `tabSales Invoice` SET einvoice_status = 'Cancelled'
        WHERE IFNULL(einvoice_status, '') = '' AND IFNULL(irn_cancelled, 0) = 1"""
    )

    set_not_applicable_status()


def set_not_applicable_status():
    sales_invoice = dontmanage.qb.DocType("Sales Invoice")

    dontmanage.qb.update(sales_invoice).set("einvoice_status", "Not Applicable").where(
        (sales_invoice.docstatus != 0)
        & (Coalesce(sales_invoice.einvoice_status, "") == "")
        & (Coalesce(sales_invoice.irn, "") == "")
    ).run()
