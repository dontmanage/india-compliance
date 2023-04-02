import dontmanage


def execute():
    if dontmanage.conf.ic_api_sandbox_mode:
        dontmanage.db.set_single_value("GST Settings", "sandbox_mode", 1)
