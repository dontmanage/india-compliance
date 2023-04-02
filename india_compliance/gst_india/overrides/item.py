import dontmanage
from dontmanage import _


def validate_hsn_code(doc, method=None):
    # HSN Code is being validated only for sales items
    if not doc.is_sales_item:
        return

    validate_hsn_code, min_hsn_digits = dontmanage.get_cached_value(
        "GST Settings",
        "GST Settings",
        ("validate_hsn_code", "min_hsn_digits"),
    )

    if not validate_hsn_code:
        return

    if not doc.gst_hsn_code:
        dontmanage.throw(
            _("HSN/SAC Code is required. Please enter a valid HSN/SAC code.").format(
                doc.item_name
            ),
            dontmanage.MandatoryError,
        )

    if len(doc.gst_hsn_code) < int(min_hsn_digits):
        dontmanage.throw(
            _(
                "HSN/SAC Code should be at least {0} digits long. Please enter a valid"
                " HSN/SAC code."
            ).format(min_hsn_digits)
        )
