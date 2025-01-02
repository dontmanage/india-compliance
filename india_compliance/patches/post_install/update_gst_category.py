import dontmanage


def execute():
    for doctype, field in (
        {
            "Sales Invoice": "billing_address_gstin",
            "Purchase Invoice": "supplier_gstin",
        }
    ).items():
        dontmanage.db.set_value(
            doctype, {field: ("in", (None, ""))}, "gst_category", "Unregistered"
        )
