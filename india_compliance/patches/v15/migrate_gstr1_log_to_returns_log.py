import dontmanage


def execute():
    if not dontmanage.db.table_exists("GSTR-1 Log"):
        return

    old = dontmanage.qb.DocType("GSTR-1 Log")
    old_docs = dontmanage.qb.from_(old).select("*").run(as_dict=True)

    for doc in old_docs:
        new_doc = dontmanage.get_doc(
            {**doc, "doctype": "GST Return Log", "name": None, "return_type": "GSTR1"}
        )
        new_doc.insert(ignore_if_duplicate=True)

    # Drop the old table
    dontmanage.db.delete("GSTR-1 Log")

    # Clear all fields saved in GSTR-1 Beta
    dontmanage.db.delete("Singles", {"doctype": "GSTR-1 Beta"})
