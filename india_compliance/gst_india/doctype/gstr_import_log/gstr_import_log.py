# Copyright (c) 2022, Resilient Tech and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage.model.document import Document
from dontmanage.utils import add_to_date


class GSTRImportLog(Document):
    pass


def create_import_log(
    gstin,
    return_type,
    return_period,
    classification=None,
    data_not_found=False,
    request_id=None,
    retry_after_mins=None,
):
    dontmanage.enqueue(
        _create_import_log,
        queue="short",
        now=dontmanage.flags.in_test,
        gstin=gstin,
        return_type=return_type,
        return_period=return_period,
        data_not_found=data_not_found,
        classification=classification,
        request_id=request_id,
        retry_after_mins=retry_after_mins,
    )


def _create_import_log(
    gstin,
    return_type,
    return_period,
    classification=None,
    data_not_found=False,
    request_id=None,
    retry_after_mins=None,
):
    doctype = "GSTR Import Log"
    fields = {
        "gstin": gstin,
        "return_type": return_type,
        "return_period": return_period,
    }

    if classification:
        fields["classification"] = classification

    if log := dontmanage.db.get_value(doctype, fields):
        log = dontmanage.get_doc(doctype, log)
    else:
        log = dontmanage.get_doc({"doctype": doctype, **fields})

    if retry_after_mins:
        log.request_time = add_to_date(None, minutes=retry_after_mins)

    log.request_id = request_id
    log.data_not_found = data_not_found
    log.last_updated_on = dontmanage.utils.now()
    log.save(ignore_permissions=True)
    if request_id:
        toggle_scheduled_jobs(False)


def toggle_scheduled_jobs(stopped):
    scheduled_job = dontmanage.db.get_value(
        "Scheduled Job Type",
        {
            "method": "india_compliance.gst_india.utils.gstr_utils.download_queued_request",
        },
    )

    if scheduled_job:
        dontmanage.db.set_value("Scheduled Job Type", scheduled_job, "stopped", stopped)
