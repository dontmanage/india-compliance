import dontmanage


def execute():
    if "eligibility_for_itc" not in dontmanage.db.get_table_columns("Purchase Invoice"):
        return

    dontmanage.db.set_value(
        "Purchase Invoice",
        {"eligibility_for_itc": "Import Of Capital Goods"},
        "eligibility_for_itc",
        "Import Of Goods",
    )
