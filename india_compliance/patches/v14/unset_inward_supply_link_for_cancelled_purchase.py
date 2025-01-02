import dontmanage

DOCTYPES = ("Purchase Invoice", "Bill of Entry")


def execute():
    for doctype in DOCTYPES:
        cancelled_doc = get_cancelled_doc(doctype)
        dontmanage.db.set_value(
            "GST Inward Supply",
            {"link_name": ("in", cancelled_doc), "link_doctype": doctype},
            {"link_name": "", "link_doctype": "", "match_status": ""},
        )


def get_cancelled_doc(doctype):
    return dontmanage.get_all(
        doctype,
        filters={"docstatus": 2},
        pluck="name",
    )
