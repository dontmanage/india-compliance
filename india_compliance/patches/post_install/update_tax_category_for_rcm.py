import dontmanage


def execute():
    tax_category = dontmanage.qb.DocType("Tax Category")

    dontmanage.qb.update(tax_category).set(tax_category.is_reverse_charge, 1).where(
        tax_category.name.isin(("Reverse Charge Out-State", "Reverse Charge In-State"))
    ).run()
