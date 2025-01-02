// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

{% include "dontmanageerp/accounts/report/sales_register/sales_register.js" %}

dontmanage.query_reports["GST Sales Register"] = dontmanage.query_reports["Sales Register"]
india_compliance.set_last_month_as_default_period(dontmanage.query_reports["GST Sales Register"]);