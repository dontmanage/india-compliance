from functools import partial

import dontmanage
from dontmanage.desk.page.setup_wizard.setup_wizard import setup_complete
from dontmanage.test_runner import make_test_objects
from dontmanage.utils import getdate
from dontmanage.utils.nestedset import get_root_of
from dontmanageerp.accounts.utils import get_fiscal_year


def before_tests():
    dontmanage.clear_cache()

    if not dontmanage.db.a_row_exists("Company"):
        today = getdate()
        year = today.year if today.month > 3 else today.year - 1

        setup_complete(
            {
                "currency": "INR",
                "full_name": "Test User",
                "company_name": "Wind Power LLP",
                "timezone": "Asia/Kolkata",
                "company_abbr": "WP",
                "industry": "Manufacturing",
                "country": "India",
                "fy_start_date": f"{year}-04-01",
                "fy_end_date": f"{year + 1}-03-31",
                "language": "English",
                "company_tagline": "Testing",
                "email": "test@example.com",
                "password": "test",
                "chart_of_accounts": "Standard",
            }
        )

    set_default_settings_for_tests()
    create_test_records()
    dontmanage.db.commit()

    dontmanage.flags.country = "India"
    dontmanage.flags.skip_test_records = True
    dontmanage.enqueue = partial(dontmanage.enqueue, now=True)


def set_default_settings_for_tests():
    # e.g. set "All Customer Groups" as the default Customer Group
    for key in ("Customer Group", "Supplier Group", "Item Group", "Territory"):
        dontmanage.db.set_default(dontmanage.scrub(key), get_root_of(key))

    # Allow Negative Stock
    dontmanage.db.set_single_value("Stock Settings", "allow_negative_stock", 1)

    # Enable Sandbox Mode in GST Settings
    dontmanage.db.set_single_value("GST Settings", "sandbox_mode", 1)


def create_test_records():
    test_records = dontmanage.get_file_json(
        dontmanage.get_app_path("india_compliance", "tests", "test_records.json")
    )

    for doctype, data in test_records.items():
        make_test_objects(doctype, data, reset=True)
        if doctype == "Company":
            add_companies_to_fiscal_year(data)


def add_companies_to_fiscal_year(data):
    fy = get_fiscal_year(getdate(), as_dict=True)
    doc = dontmanage.get_doc("Fiscal Year", fy.name)
    fy_companies = [row.company for row in doc.companies]

    for company in data:
        if (company_name := company["company_name"]) not in fy_companies:
            doc.append("companies", {"company": company_name})

    doc.save(ignore_permissions=True)
