class PaymentPage:
    """결제 화면 (/payment)과 결제 완료 화면 (/payment_done)."""

    def __init__(self, page):
        self.page = page
        self.name_on_card_input = page.locator("[data-qa='name-on-card']")
        self.card_number_input = page.locator("[data-qa='card-number']")
        self.cvc_input = page.locator("[data-qa='cvc']")
        self.expiry_month_input = page.locator("[data-qa='expiry-month']")
        self.expiry_year_input = page.locator("[data-qa='expiry-year']")
        self.pay_button = page.locator("[data-qa='pay-button']")

        self.order_placed = page.locator("[data-qa='order-placed']")
        self.order_confirmed_message = page.get_by_text("Congratulations! Your order has been confirmed!")

    def pay(self, card):
        self.name_on_card_input.fill(card["name"])
        self.card_number_input.fill(card["number"])
        self.cvc_input.fill(card["cvc"])
        self.expiry_month_input.fill(card["month"])
        self.expiry_year_input.fill(card["year"])
        self.pay_button.click()
