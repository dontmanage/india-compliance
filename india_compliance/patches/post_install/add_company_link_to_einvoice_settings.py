import dontmanage
from dontmanage.query_builder.functions import IfNull


def execute():
    """
    update Company of E Invoice User from Dyanamic Link Table in Address
    """

    if not dontmanage.db.table_exists("E Invoice User"):
        return

    user = dontmanage.qb.DocType("E Invoice User", alias="user")
    address = dontmanage.qb.DocType("Address", alias="address")
    dynamic_link = dontmanage.qb.DocType("Dynamic Link", alias="dynamic_link")
    (
        dontmanage.qb.update(user)
        .join(address)
        .on(address.gstin == user.gstin)
        .join(dynamic_link)
        .on(
            (dynamic_link.parent == address.name)
            & (dynamic_link.link_doctype == "Company")
        )
        .set(user.company, dynamic_link.link_name)
        .where(IfNull(user.company, "") == "")
        .run()
    )
