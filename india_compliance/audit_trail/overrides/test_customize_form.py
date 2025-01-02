import re

import dontmanage
from dontmanage.tests.utils import DontManageTestCase


class TestCustomizeFormAuditTrail(DontManageTestCase):
    def test_validate_customize_form(self):
        customize_frm = self.get_customize_form()
        customize_frm.doc_type = "Purchase Invoice"
        customize_frm.save_customization()

        dontmanage.db.set_single_value("Accounts Settings", "enable_audit_trail", 1)

        customize_frm.track_changes = 0
        self.assertRaisesRegex(
            dontmanage.ValidationError,
            re.compile(r"^(Cannot disable Track Changes for*)"),
            customize_frm.save_customization,
        )
        dontmanage.db.set_single_value("Accounts Settings", "enable_audit_trail", 0)

    def get_customize_form(self, doctype=None):
        d = dontmanage.get_doc("Customize Form")
        if doctype:
            d.doc_type = doctype
        d.run_method("fetch_to_customize")
        return d
