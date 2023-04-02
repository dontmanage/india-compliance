dontmanage.ui.form.on("Payment Entry", {
	company: function(frm) {
		dontmanage.call({
			'method': 'dontmanage.contacts.doctype.address.address.get_default_address',
			'args': {
				'doctype': 'Company',
				'name': frm.doc.company
			},
			'callback': function(r) {
				frm.set_value('company_address', r.message);
			}
		});
	},

	party: function(frm) {
		if (frm.doc.party_type == "Customer" && frm.doc.party) {
			dontmanage.call({
				'method': 'dontmanage.contacts.doctype.address.address.get_default_address',
				'args': {
					'doctype': 'Customer',
					'name': frm.doc.party
				},
				'callback': function(r) {
					frm.set_value('customer_address', r.message);
				}
			});
		}
	}
});
