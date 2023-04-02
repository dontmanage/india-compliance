dontmanage.ui.form.on("Journal Entry", {
	refresh: function(frm) {
		frm.set_query('company_address', function(doc) {
			if(!doc.company) {
				dontmanage.throw(__('Please set Company'));
			}

			return {
				query: 'dontmanage.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: 'Company',
					link_name: doc.company
				}
			};
		});
	}
});
