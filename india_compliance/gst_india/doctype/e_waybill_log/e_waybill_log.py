# Copyright (c) 2022, Resilient Tech and contributors
# For license information, please see license.txt

import dontmanage
from dontmanage import _
from dontmanage.model.document import Document

from india_compliance.gst_india.utils import send_updated_doc
from india_compliance.gst_india.utils.e_waybill import _fetch_e_waybill_data


class eWaybillLog(Document):
    def before_print(self, print_settings=None):
        if self.data and self.is_latest_data:
            return

        doc = dontmanage.get_doc(self.reference_doctype, self.reference_name)
        _fetch_e_waybill_data(doc, self)
        send_updated_doc(self)
        dontmanage.msgprint(
            _("Fetched latest e-Waybill data"), alert=True, indicator="green"
        )
