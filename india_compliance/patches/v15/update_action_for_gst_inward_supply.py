import dontmanage


def execute():
    # Discard the action "Accept Supplier Values"
    dontmanage.db.set_value(
        "GST Inward Supply",
        {"action": ["in", ["Accept My Values", "Accept Supplier Values"]]},
        "action",
        "Accept",
    )
