# Copyright (c) 2017, DontManage and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document
from dontmanage.utils import getdate

from india_compliance.gst_india.constants import GST_ACCOUNT_FIELDS
from india_compliance.gst_india.constants.custom_fields import (
    E_INVOICE_FIELDS,
    E_WAYBILL_FIELDS,
    SALES_REVERSE_CHARGE_FIELDS,
)
from india_compliance.gst_india.page.india_compliance_account import (
    _disable_api_promo,
    post_login,
)
from india_compliance.gst_india.utils import can_enable_api
from india_compliance.gst_india.utils.custom_fields import toggle_custom_fields


class GSTSettings(Document):
    def onload(self):
        if can_enable_api(self) or dontmanage.db.get_global("ic_api_promo_dismissed"):
            return

        self.set_onload("can_show_promo", True)

    def validate(self):
        self.update_dependant_fields()
        self.validate_enable_api()
        self.validate_gst_accounts()
        self.validate_e_invoice_applicability_date()
        self.validate_credentials()
        self.clear_api_auth_session()

    def clear_api_auth_session(self):
        if self.has_value_changed("api_secret") and self.api_secret:
            post_login()

    def update_dependant_fields(self):
        if self.attach_e_waybill_print:
            self.fetch_e_waybill_data = 1

        if self.enable_e_invoice:
            self.auto_generate_e_waybill = self.auto_generate_e_invoice

    def on_update(self):
        self.update_custom_fields()

        # clear session boot cache
        dontmanage.cache().delete_keys("bootinfo")

    def validate_gst_accounts(self):
        account_list = []
        company_wise_account_types = {}

        for row in self.gst_accounts:
            # Validate Duplicate Accounts
            for fieldname in GST_ACCOUNT_FIELDS:
                account = row.get(fieldname)
                if not account:
                    continue

                if account in account_list:
                    dontmanage.throw(
                        _("Row #{0}: Account {1} appears multiple times").format(
                            row.idx,
                            dontmanage.bold(account),
                        )
                    )

                account_list.append(account)

            # Validate Duplicate Account Types for each Company
            account_types = company_wise_account_types.setdefault(row.company, [])
            if row.account_type in account_types:
                dontmanage.throw(
                    _(
                        "Row #{0}: Account Type {1} appears multiple times for {2}"
                    ).format(
                        row.idx,
                        dontmanage.bold(row.account_type),
                        dontmanage.bold(row.company),
                    )
                )

            account_types.append(row.account_type)

    def update_custom_fields(self):
        if self.has_value_changed("enable_e_waybill"):
            toggle_custom_fields(E_WAYBILL_FIELDS, self.enable_e_waybill)

        if self.has_value_changed("enable_e_invoice"):
            toggle_custom_fields(E_INVOICE_FIELDS, self.enable_e_invoice)

        if self.has_value_changed("enable_reverse_charge_in_sales"):
            toggle_custom_fields(
                SALES_REVERSE_CHARGE_FIELDS, self.enable_reverse_charge_in_sales
            )

    def validate_e_invoice_applicability_date(self):
        if not self.enable_api or not self.enable_e_invoice:
            return

        if not self.e_invoice_applicable_from:
            dontmanage.throw(
                _("{0} is mandatory for enabling e-Invoice").format(
                    dontmanage.bold(self.meta.get_label("e_invoice_applicable_from"))
                )
            )

        if getdate(self.e_invoice_applicable_from) < getdate("2021-01-01"):
            dontmanage.throw(
                _("{0} cannot be before 2021-01-01").format(
                    dontmanage.bold(self.meta.get_label("e_invoice_applicable_from"))
                )
            )

    def validate_credentials(self):
        if not self.enable_api:
            return

        for credential in self.credentials:
            if credential.service == "Returns" or credential.password:
                continue

            dontmanage.throw(
                _(
                    "Row #{0}: Password is required when setting a GST Credential"
                    " for {1}"
                ).format(credential.idx, credential.service),
                dontmanage.MandatoryError,
                _("Missing Required Field"),
            )

        if (self.enable_e_invoice or self.enable_e_waybill) and all(
            credential.service != "e-Waybill / e-Invoice"
            for credential in self.credentials
        ):
            dontmanage.msgprint(
                # TODO: Add Link to Documentation.
                _(
                    "Please set credentials for e-Waybill / e-Invoice to use API"
                    " features"
                ),
                indicator="yellow",
                alert=True,
            )

    def validate_enable_api(self):
        if (
            self.enable_api
            and self.has_value_changed("enable_api")
            and not can_enable_api(self)
        ):
            dontmanage.throw(
                _(
                    "Please counfigure your India Compliance Account to "
                    "enable API features"
                )
            )


@dontmanage.whitelist()
def disable_api_promo():
    if dontmanage.has_permission("GST Settings", "write"):
        _disable_api_promo()
