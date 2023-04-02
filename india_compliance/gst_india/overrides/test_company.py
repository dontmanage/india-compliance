import re

import dontmanage
from dontmanage.tests.utils import DontManageTestCase

from india_compliance.gst_india.overrides.company import make_default_tax_templates


class TestCompanyFixtures(DontManageTestCase):
    @classmethod
    def setUpClass(cls):
        dontmanage.db.savepoint("before_test_company")

        cls.company = dontmanage.new_doc("Company")
        cls.company.update(
            {
                "abbr": "_TC",
                "company_name": "_Test Company",
                "country": "India",
                "default_currency": "INR",
                "doctype": "Company",
                "domain": "Manufacturing",
                "chart_of_accounts": "Standard",
                "enable_perpetual_inventory": 0,
                "gstin": "24AAQCA8719H1ZC",
                "gst_category": "Registered Regular",
            }
        )
        cls.company.insert()

    @classmethod
    def tearDownClass(cls):
        dontmanage.db.rollback(save_point="before_test_company")

    def test_company_exist(self):
        self.assertRaisesRegex(
            dontmanage.exceptions.ValidationError,
            re.compile(r"^(.*does not exist yet.*)$"),
            make_default_tax_templates,
            "Random Company Name",
        )

    def test_tax_defaults_setup(self):
        # Check for tax category creations.
        self.assertTrue(dontmanage.db.exists("Tax Category", "Reverse Charge In-State"))
