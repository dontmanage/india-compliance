import re

import dontmanage
from dontmanage.tests.utils import DontManageTestCase

from india_compliance.gst_india.utils.tests import create_sales_invoice


class TestVersion(DontManageTestCase):
    def test_validate_version_where_audit_trail_enabled(self):
        # enable audit trail
        dontmanage.db.set_single_value("Accounts Settings", "enable_audit_trail", 1)

        doc = create_sales_invoice(do_not_submit=True)
        doc.items[0].qty = 2
        doc.save(ignore_version=False)
        doc.submit()

        version = dontmanage.get_doc(
            "Version", {"ref_doctype": doc.doctype, "docname": doc.name}
        )

        version.ref_doctype = "Address"

        self.assertRaisesRegex(
            dontmanage.ValidationError,
            re.compile(r"^(Cannot alter Versions of.*)"),
            version.save,
        )

        self.assertRaisesRegex(
            dontmanage.ValidationError,
            re.compile(r"^(Cannot alter Versions of.*)"),
            version.delete,
        )

        # disable audit trail
        dontmanage.db.set_single_value("Accounts Settings", "enable_audit_trail", 0)

    def test_validate_version_where_audit_trail_disabled(self):
        doc = create_sales_invoice(do_not_submit=True)
        doc.items[0].qty = 2
        doc.save(ignore_version=False)
        doc.submit()

        version = dontmanage.get_doc(
            "Version", {"ref_doctype": doc.doctype, "docname": doc.name}
        )

        version.ref_doctype = "Address"

        version.save()
        version.delete()
