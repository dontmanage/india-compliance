import dontmanage


def execute():
    reverse_charge_tax_category = dontmanage.db.get_all(
        "Tax Category",
        filters={"is_reverse_charge": "1"},
        pluck="name",
    )

    if not reverse_charge_tax_category:
        return

    dontmanage.db.set_value(
        "Supplier",
        {"tax_category": ("in", reverse_charge_tax_category)},
        "is_reverse_charge_applicable",
        1,
    )
