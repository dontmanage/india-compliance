import re

import dontmanage
from dontmanage.tests.utils import DontManageTestCase


class TestAccountsSettings(DontManageTestCase):
    def test_validate_change_in_enable_audit_trail_and_validate_delete_linked_ledger_entries(
        self,
    ):
        doc = dontmanage.get_doc("Accounts Settings")

        doc.enable_audit_trail = 1
        doc.save()

        doc.delete_linked_ledger_entries = 1
        self.assertRaisesRegex(
            dontmanage.ValidationError,
            re.compile(r"cannot be enabled to ensure Audit Trail integrity$"),
            doc.save,
        )

        doc.reload()

        doc.enable_audit_trail = 0
        self.assertRaisesRegex(
            dontmanage.ValidationError,
            re.compile(r"^(Audit Trail cannot be disabled once enabled*)"),
            doc.save,
        )
