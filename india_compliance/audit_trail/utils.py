import dontmanage
import dontmanage.defaults


def is_audit_trail_enabled():
    return bool(dontmanage.db.get_single_value("Accounts Settings", "enable_audit_trail"))


def get_audit_trail_doctypes():
    return set(dontmanage.get_hooks("audit_trail_doctypes"))


def enqueue_disable_audit_trail_notification():
    dontmanage.enqueue(
        "india_compliance.audit_trail.utils.disable_audit_trail_notification",
        queue="short",
    )


@dontmanage.whitelist(methods=["POST"])
def disable_audit_trail_notification():
    dontmanage.defaults.clear_user_default("needs_audit_trail_notification")


@dontmanage.whitelist(methods=["POST"])
def enable_audit_trail():
    accounts_settings = dontmanage.get_doc("Accounts Settings")
    accounts_settings.enable_audit_trail = 1
    accounts_settings.flags.ignore_version = True
    accounts_settings.save()
