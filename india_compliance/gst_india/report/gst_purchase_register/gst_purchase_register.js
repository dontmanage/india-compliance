// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

{% include "dontmanageerp/accounts/report/purchase_register/purchase_register.js" %}

dontmanage.query_reports["GST Purchase Register"] = dontmanage.query_reports["Purchase Register"]
india_compliance.set_last_month_as_default_period(dontmanage.query_reports["GST Purchase Register"]);