import dontmanage

from india_compliance.gst_india.setup import EMAIL_TEMPLATE_DATA


def execute():
    doctype = EMAIL_TEMPLATE_DATA.pop("doctype")
    name = EMAIL_TEMPLATE_DATA.pop("name")

    if not dontmanage.db.exists(doctype, name):
        return

    dontmanage.db.set_value(doctype, name, EMAIL_TEMPLATE_DATA)
