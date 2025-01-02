import dontmanage


def execute():
    boe_item = dontmanage.qb.DocType("Bill of Entry Item", alias="boe_item")
    pi_item = dontmanage.qb.DocType("Purchase Invoice Item")

    (
        dontmanage.qb.update(boe_item)
        .left_join(pi_item)
        .on(pi_item.name == boe_item.pi_detail)
        .set(boe_item.gst_hsn_code, pi_item.gst_hsn_code)
        .set(boe_item.qty, pi_item.qty)
        .set(boe_item.uom, pi_item.uom)
        .where(boe_item.docstatus == 1)
        .run()
    )
