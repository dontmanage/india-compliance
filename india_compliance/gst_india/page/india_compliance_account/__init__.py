import json
import random

import dontmanage
from dontmanage.utils.password import (
    get_decrypted_password,
    remove_encrypted_password,
    set_encrypted_password,
)


@dontmanage.whitelist()
def get_api_secret():
    dontmanage.only_for("System Manager")

    return get_decrypted_password(
        "GST Settings",
        "GST Settings",
        fieldname="api_secret",
        raise_exception=False,
    )


@dontmanage.whitelist()
def set_api_secret(api_secret: str):
    dontmanage.only_for("System Manager")

    if not api_secret:
        return logout()

    set_encrypted_password(
        "GST Settings", "GST Settings", api_secret, fieldname="api_secret"
    )
    dontmanage.db.set_value("GST Settings", None, "api_secret", "*" * random.randint(8, 16))
    post_login()


def post_login():
    _set_auth_session(None)
    _disable_api_promo()


def logout():
    remove_encrypted_password("GST Settings", "GST Settings", fieldname="api_secret")
    dontmanage.db.set_value("GST Settings", None, "api_secret", None)


@dontmanage.whitelist()
def get_auth_session():
    dontmanage.only_for("System Manager")

    session = dontmanage.db.get_global("ic_auth_session")
    return session and json.loads(session)


@dontmanage.whitelist()
def set_auth_session(session: str = None):
    dontmanage.only_for("System Manager")

    if not session:
        _set_auth_session(None)
        return

    if not isinstance(session, str):
        session = json.dumps(session)

    _set_auth_session(session)


def _set_auth_session(session):
    dontmanage.db.set_global("ic_auth_session", session)


def _disable_api_promo():
    dontmanage.db.set_global("ic_api_promo_dismissed", 1)
