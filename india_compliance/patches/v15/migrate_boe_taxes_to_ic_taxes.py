import dontmanage
from dontmanage.model.document import bulk_insert
from dontmanage.model.naming import _generate_random_string


def execute():
    if not dontmanage.db.table_exists("Bill of Entry Taxes"):
        return

    boe_taxes = dontmanage.qb.DocType("Bill of Entry Taxes")
    boe_taxes_docs = dontmanage.qb.from_(boe_taxes).select("*").run(as_dict=True)

    ic_taxes_names = set(
        dontmanage.get_all("India Compliance Taxes and Charges", pluck="name")
    )
    ic_taxes = []

    for doc in boe_taxes_docs:
        ic_taxes_doc = dontmanage.get_doc(
            {
                **doc,
                "doctype": "India Compliance Taxes and Charges",
                "name": set_name(doc.name, ic_taxes_names),
                "base_total": doc.total,
            }
        )

        ic_taxes.append(ic_taxes_doc)

    bulk_insert("India Compliance Taxes and Charges", ic_taxes)

    # Drop the old table
    dontmanage.db.delete("Bill of Entry Taxes")


def set_name(name, names):
    new_name = name
    while new_name in names:
        new_name = _generate_random_string(10)

    names.add(new_name)
    return new_name
