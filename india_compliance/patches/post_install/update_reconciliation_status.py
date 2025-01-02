import dontmanage
from dontmanage.query_builder.functions import IfNull


def execute():
    PI = dontmanage.qb.DocType("Purchase Invoice")
    PI_ITEM = dontmanage.qb.DocType("Purchase Invoice Item")
    BOE = dontmanage.qb.DocType("Bill of Entry")

    (
        dontmanage.qb.update(PI)
        .set(PI.reconciliation_status, "Not Applicable")
        .join(PI_ITEM)
        .on(PI.name == PI_ITEM.parent)
        .where(PI.docstatus == 1)
        .where(
            (IfNull(PI.supplier_gstin, "") == "")
            | (
                IfNull(PI.gst_category, "").isin(
                    ["Registered Composition", "Unregistered", "Overseas"]
                )
            )
            | (IfNull(PI.supplier_gstin, "") == PI.company_gstin)
            | (IfNull(PI.is_opening, "") == "Yes")
            | (PI_ITEM.gst_treatment == "Non-GST")
        )
        .run()
    )

    (
        dontmanage.qb.update(PI)
        .set(PI.reconciliation_status, "Unreconciled")
        .where(PI.docstatus == 1)
        .where(IfNull(PI.reconciliation_status, "") == "")
        .run()
    )

    (
        dontmanage.qb.update(BOE)
        .set(BOE.reconciliation_status, "Unreconciled")
        .where(BOE.docstatus == 1)
        .run()
    )
