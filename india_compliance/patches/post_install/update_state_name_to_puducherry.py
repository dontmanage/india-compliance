import dontmanage


def execute():
    dontmanage.db.set_value(
        "Address",
        {"gst_state": "Pondicherry"},
        {
            "gst_state": "Puducherry",
            "state": "Puducherry",
        },
    )
