# Copyright (c) 2017, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document


class GSTHSNCode(Document):
    pass


@dontmanage.whitelist()
def update_taxes_in_item_master(taxes, hsn_code):
    items = dontmanage.get_list("Item", filters={"gst_hsn_code": hsn_code})

    taxes = dontmanage.parse_json(taxes)
    dontmanage.enqueue(update_item_document, items=items, taxes=taxes)
    return 1


def update_item_document(items, taxes):
    for item in items:
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
                },
            )
            item_to_be_updated.save()
