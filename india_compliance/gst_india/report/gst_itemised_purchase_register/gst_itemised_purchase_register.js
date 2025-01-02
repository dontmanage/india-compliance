// Copyright (c) 2016, DontManage and contributors
// For license information, please see license.txt
/* eslint-disable */

{% include "dontmanageerp/accounts/report/item_wise_purchase_register/item_wise_purchase_register.js" %}

dontmanage.query_reports["GST Itemised Purchase Register"] = dontmanage.query_reports["Item-wise Purchase Register"]
india_compliance.set_last_month_as_default_period(dontmanage.query_reports["GST Itemised Purchase Register"]);
