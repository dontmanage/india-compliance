import dontmanage


def execute():
    settings = dontmanage.get_single("GST Settings")

    dontmanage.db.set_value(
        "Scheduled Job Type",
        {
            "method": "india_compliance.gst_india.doctype.purchase_reconciliation_tool.purchase_reconciliation_tool.auto_refresh_authtoken"
        },
        "stopped",
        not settings.enable_auto_reconciliation,
    )
