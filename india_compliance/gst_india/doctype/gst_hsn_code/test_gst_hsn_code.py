# Copyright (c) 2017, DontManage and Contributors
# See license.txt
import re

import dontmanage
from dontmanage.tests.utils import DontManageTestCase, change_settings

from india_compliance.gst_india.doctype.gst_hsn_code.gst_hsn_code import (
    update_taxes_in_item_master,
)


class TestGSTHSNCode(DontManageTestCase):
    @change_settings("GST Settings", {"validate_hsn_code": 0})
    def test_validate_hsn_when_validate_hsn_code_disabled(self):
        doc = dontmanage.get_doc({"doctype": "GST HSN Code", "hsn_code": "1"})
        doc.save()
        self.assertDocumentEqual({"hsn_code": 1}, dontmanage.get_doc("GST HSN Code", "1"))

    def test_validate_hsn_with_invalid_hsn_length(self):
        doc = dontmanage.get_doc({"doctype": "GST HSN Code", "hsn_code": "100"})
        self.assertRaisesRegex(
            dontmanage.ValidationError,
            re.compile(r"^(HSN/SAC Code should be .*)"),
            doc.save,
        )

    def test_update_taxes_in_item_master(self):
        taxes = [{"item_tax_template": "GST 12% - _TIUC", "tax_category": "In-State"}]
        doc = dontmanage.get_doc(
            {"doctype": "GST HSN Code", "hsn_code": "100000", "taxes": taxes}
        )
        doc.save()
        item = dontmanage.get_doc(
            {
                "doctype": "Item",
                "item_code": "SKU9999",
                "item_group": "All Item Groups",
                "gst_hsn_code": "100000",
                "stock_uom": "Nos",
            }
        )
        item.save()
        update_taxes_in_item_master(taxes=taxes, hsn_code="100000")
        self.assertDocumentEqual(taxes[0], dontmanage.get_doc("Item", "SKU9999").taxes[0])
