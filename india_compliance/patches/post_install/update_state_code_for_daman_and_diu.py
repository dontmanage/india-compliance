import dontmanage


def execute():
    address = dontmanage.qb.DocType("Address")

    (
        dontmanage.qb.update(address)
        .set(address.gst_state, "Dadra and Nagar Haveli and Daman and Diu")
        .set(address.gst_state_number, "26")
        .where(address.gst_state == "Daman and Diu")
    ).run()
