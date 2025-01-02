import dontmanage


def execute():
    if not dontmanage.db.has_column("Company Print Options", "autofield"):
        return

    doc = dontmanage.qb.DocType("Company Print Options")

    (
        dontmanage.qb.update(doc)
        .set(doc.print_label, doc.autofield)
        .set(doc.print_value, doc.autofield_value)
        .run()
    )
