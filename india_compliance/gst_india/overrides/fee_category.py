import dontmanage


def before_update(doc, method=None):
    if doc.gst_hsn_code:
        dontmanage.flags.category_hsn_code = doc.gst_hsn_code
