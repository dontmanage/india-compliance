import dontmanage


def execute():
    for doctype in ("Customer", "Supplier", "Address"):
        if not dontmanage.db.has_column(doctype, "gst_category"):
            continue

        dontmanage.db.set_value(
            doctype, {"gst_category": "Consumer"}, "gst_category", "Unregistered"
        )
