// Copyright (c) 2017, DontManage and contributors
// For license information, please see license.txt

dontmanage.ui.form.on('GST HSN Code', {
	refresh: function(frm) {
		if(! frm.doc.__islocal && frm.doc.taxes.length){
			frm.add_custom_button(__('Update Taxes for Items'), function(){
				dontmanage.confirm(
					'Are you sure? It will overwrite taxes for all items with HSN Code <b>'+frm.doc.name+'</b>.',
					function(){
						dontmanage.call({
							args:{
								taxes: frm.doc.taxes,
								hsn_code: frm.doc.name
							},
							method: 'india_compliance.gst_india.doctype.gst_hsn_code.gst_hsn_code.update_taxes_in_item_master',
							callback: function(r) {
								if(r.message){
									dontmanage.show_alert(__('Item taxes updated'));
								}
							}
						});
					}
				);
			});
		}
	}
});
