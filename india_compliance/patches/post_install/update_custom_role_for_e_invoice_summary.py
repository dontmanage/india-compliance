import dontmanage


def execute():
    dontmanage.db.set_value(
        "Custom Role", {"report": "E-Invoice Summary"}, "report", "e-Invoice Summary"
    )
