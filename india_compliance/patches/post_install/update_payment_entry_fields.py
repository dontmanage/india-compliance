import dontmanage

from india_compliance.gst_india.utils.custom_fields import delete_old_fields


def execute():
    if not dontmanage.db.has_column("Payment Entry", "customer_gstin"):
        return

    payment_entry = dontmanage.qb.DocType("Payment Entry")
    dontmanage.qb.update(payment_entry).set(
        payment_entry.billing_address_gstin, payment_entry.customer_gstin
    ).run()

    delete_old_fields("customer_gstin", "Payment Entry")
