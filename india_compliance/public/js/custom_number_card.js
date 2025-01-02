let DontManageNumberCard = dontmanage.widget.widget_factory.number_card;

class CustomNumberCard extends DontManageNumberCard {
	render_number() {
		if (
			[
				"Pending e-Waybill",
				"Pending e-Invoices",
				"Invoice Cancelled But Not e-Invoice",
			].includes(this.card_doc.name) &&
			!this.formatted_number
		)
			this.card_doc.color = null;

		super.render_number();
	}
}

dontmanage.widget.widget_factory.number_card = CustomNumberCard;
