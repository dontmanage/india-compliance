import dontmanage


def execute():
    if not dontmanage.db.has_column("GSTR 3B Report", "month"):
        return

    # Update month_or_quarter from month field
    gstr3b_report = dontmanage.qb.DocType("GSTR 3B Report")

    (
        dontmanage.qb.update(gstr3b_report)
        .set(gstr3b_report.month_or_quarter, gstr3b_report.month)
        .run()
    )

    # Update company_gstin based on company_address
    addresses = dontmanage.get_all("GSTR 3B Report", pluck="company_address", distinct=True)

    for address in addresses:
        dontmanage.db.set_value(
            "GSTR 3B Report",
            {"company_address": address},
            "company_gstin",
            get_gstin_based_on_address(address),
        )


def get_gstin_based_on_address(address):
    """Get GSTIN based on company_address or company"""
    return (
        dontmanage.db.get_value(
            "Address",
            address,
            "gstin",
        )
        or ""
    )
