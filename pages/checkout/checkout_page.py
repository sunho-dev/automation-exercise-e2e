from pages.cart.cart_page import to_price


class CheckoutPage:
    """주문 확인 화면 (/checkout)."""

    def __init__(self, page):
        self.page = page
        self.delivery_address = page.locator("#address_delivery")
        self.total_amount = page.locator("#cart_info tbody tr", has_text="Total Amount").locator(".cart_total_price")
        self.place_order_button = page.locator("a[href='/payment']")

    def get_total_amount(self):
        return to_price(self.total_amount.inner_text())

    def place_order(self):
        self.place_order_button.click()
