import dontmanage


def on_change(doc, method=None):
    dontmanage.cache.delete_value("tax_withholding_accounts")


def get_tax_withholding_accounts(company):
    def _get_tax_withholding_accounts():
        return set(
            dontmanage.get_all(
                "Tax Withholding Account", pluck="account", filters={"company": company}
            )
        )

    return dontmanage.cache.hget(
        "tax_withholding_accounts", company, generator=_get_tax_withholding_accounts
    )
