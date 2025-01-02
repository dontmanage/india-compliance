import dontmanage


def execute():
    doc = dontmanage.qb.DocType("GSTR 3B Report")
    dontmanage.qb.update(doc).set(doc.generation_status, "Generated").where(
        doc.generation_status.isnull()
    ).run()
