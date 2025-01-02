import dontmanage


def execute():
    if dontmanage.db.has_column("GST Inward Supply", "is_downloaded_from_2a"):
        # set "is_downloaded_from_2a" to "1" for all GST Inward Supply
        dontmanage.db.set_value(
            "GST Inward Supply", {"name": ["is", "set"]}, "is_downloaded_from_2a", 1
        )

    if dontmanage.db.has_column("GST Inward Supply", "is_downloaded_from_2b"):
        # set "is_downloaded_from_2b" to "1" where 2B return period is set
        dontmanage.db.set_value(
            "GST Inward Supply",
            {"return_period_2b": ["is", "set"]},
            "is_downloaded_from_2b",
            1,
        )
