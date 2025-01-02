import re

import dontmanage
from dontmanage.tests.utils import DontManageTestCase


class TestPropertySetter(DontManageTestCase):
    def test_validate_property_setter_where_audit_trail_enabled_and_doc_is_protected(
        self,
    ):
        dontmanage.db.set_single_value("Accounts Settings", "enable_audit_trail", 1)
        doc = dontmanage.get_doc(
            {
                "doctype": "Property Setter",
                "doctype_or_field": "DocType",
                "doc_type": "Purchase Invoice",
                "property": "track_changes",
                "value": 1,
            },
        )
        doc.save()
        doc.value = 0

        self.assertRaisesRegex(
            dontmanage.ValidationError,
            re.compile(r"^(Cannot change the Track Changes property for*)"),
            doc.save,
        )

        self.assertRaisesRegex(
            dontmanage.ValidationError,
            re.compile(r"^(Cannot change the Track Changes property for*)"),
            doc.delete,
        )
        doc.reload()
        doc.doc_type = "Address"
        self.assertRaisesRegex(
            dontmanage.ValidationError,
            re.compile(r"^(Cannot change the Track Changes property for*)"),
            doc.save,
        )
        dontmanage.db.set_single_value("Accounts Settings", "enable_audit_trail", 0)
        doc.delete()
