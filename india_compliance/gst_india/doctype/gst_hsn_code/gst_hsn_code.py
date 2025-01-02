# Copyright (c) 2017, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document

from india_compliance.gst_india.utils import (
    get_hsn_settings,
    join_list_with_custom_separators,
)


class GSTHSNCode(Document):
    def validate(self):
        validate_hsn_code(self.hsn_code)


@dontmanage.whitelist()
def update_taxes_in_item_master(taxes, hsn_code):
    dontmanage.enqueue(update_item_document, taxes=taxes, hsn_code=hsn_code, queue="long")
    return 1


def update_item_document(taxes, hsn_code):
    taxes = dontmanage.parse_json(taxes)
    items = dontmanage.get_list("Item", filters={"gst_hsn_code": hsn_code})

    for index, item in enumerate(items):
        item_to_be_updated = dontmanage.get_doc("Item", item.name)
        item_to_be_updated.taxes = []
        for tax in taxes:
            tax = dontmanage._dict(tax)
            item_to_be_updated.append(
                "taxes",
                {
                    "item_tax_template": tax.item_tax_template,
                    "tax_category": tax.tax_category,
                    "valid_from": tax.valid_from,
                    "minimum_net_rate": tax.minimum_net_rate,
                    "maximum_net_rate": tax.maximum_net_rate,
                },
            )

        item_to_be_updated.save()

        if index % 10000 == 0:
            dontmanage.db.commit()  # nosemgrep


def validate_hsn_code(hsn_code):
    validate_hsn_code, valid_hsn_length = get_hsn_settings()

    if not validate_hsn_code:
        return

    if not hsn_code:
        dontmanage.throw(
            _("HSN/SAC Code is required. Please enter a valid HSN/SAC code."),
            dontmanage.MandatoryError,
        )

    if len(hsn_code) not in valid_hsn_length:
        dontmanage.throw(
            _(
                "HSN/SAC Code should be {0} digits long. Please enter a valid"
                " HSN/SAC code."
            ).format(join_list_with_custom_separators(valid_hsn_length)),
            title=_("Invalid HSN/SAC"),
        )
