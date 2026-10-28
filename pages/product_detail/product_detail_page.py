class ProductDetailPage:
    """상품 상세 화면 (/product_details/<id>)."""

    def __init__(self, page):
        self.page = page
        self.product_name = page.locator(".product-information h2")
        self.quantity_input = page.locator("#quantity")
        self.add_to_cart_button = page.locator("button.cart")
        self.added_modal = page.locator("#cartModal")
        self.continue_shopping_button = self.added_modal.locator(".close-modal")

    def open(self, product_id):
        self.page.goto(f"/product_details/{product_id}")

    def get_product_name(self):
        return self.product_name.inner_text()

    def add_to_cart(self, quantity=1):
        self.quantity_input.fill(str(quantity))
        self.add_to_cart_button.click()
        self.added_modal.wait_for(state="visible")

    def continue_shopping(self):
        self.continue_shopping_button.click()
        self.added_modal.wait_for(state="hidden")
