// Copyright (c) 2023, Resilient Tech and contributors
// For license information, please see license.txt

dontmanage.query_reports["Bill of Entry Summary"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 1,
            "default": dontmanage.defaults.get_user_default("Company")
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": dontmanage.datetime.add_months(dontmanage.datetime.get_today(), -1),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": dontmanage.datetime.get_today(),
            "reqd": 1
        },
    ]
}