class ProductsPage:
    """상품 목록 화면 (/products)."""

    def __init__(self, page):
        self.page = page
        self.product_names = page.locator(".productinfo p")
        self.add_to_cart_buttons = page.locator(".productinfo .add-to-cart")
        self.added_modal = page.locator("#cartModal")
        self.view_cart_link = self.added_modal.get_by_text("View Cart")
        self.continue_shopping_button = self.added_modal.locator(".close-modal")

    def open(self):
        self.page.goto("/products")

    def get_product_name(self, index=0):
        return self.product_names.nth(index).inner_text()

    def add_to_cart(self, index=0):
        """index번째 상품을 담는다. 'Added!' 팝업이 떠야 담기 요청이 끝난 것이다."""
        self.add_to_cart_buttons.nth(index).click()
        self.added_modal.wait_for(state="visible")

    def view_cart(self):
        self.view_cart_link.click()

    def continue_shopping(self):
        self.continue_shopping_button.click()
        self.added_modal.wait_for(state="hidden")
