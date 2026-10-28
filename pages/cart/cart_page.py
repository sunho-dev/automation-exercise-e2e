def to_price(text):
    """'Rs. 500' → 500"""
    return int(text.replace("Rs.", "").strip())


class CartPage:
    """장바구니 화면 (/view_cart)."""

    def __init__(self, page):
        self.page = page
        self.rows = page.locator("#cart_info_table tbody tr")
        self.proceed_to_checkout_button = page.locator(".check_out")
        self.checkout_modal = page.locator("#checkoutModal")
        self.register_login_link = self.checkout_modal.locator("a[href='/login']")
        self.empty_cart_message = page.locator("#empty_cart")

    def open(self):
        self.page.goto("/view_cart")

    def row(self, product_name):
        return self.rows.filter(has_text=product_name)

    def get_item(self, product_name):
        """상품 행의 가격·수량·합계를 숫자로 읽는다."""
        row = self.row(product_name)
        return {
            "price": to_price(row.locator(".cart_price").inner_text()),
            "quantity": int(row.locator(".cart_quantity").inner_text()),
            "total": to_price(row.locator(".cart_total").inner_text()),
        }

    def wait_until_ready(self):
        """삭제·결제 팝업은 페이지 스크립트가 처리한다.
        버튼이 보여도 스크립트 로딩 전에 누르면 아무 일도 일어나지 않으므로 로딩 완료를 기다린다."""
        self.page.wait_for_load_state("load")

    def delete(self, product_name):
        self.wait_until_ready()
        self.row(product_name).locator(".cart_quantity_delete").click()

    def proceed_to_checkout(self):
        self.wait_until_ready()
        self.proceed_to_checkout_button.click()

    def go_to_register_login(self):
        """비로그인 상태에서 결제를 누르면 뜨는 팝업의 Register / Login 링크."""
        self.register_login_link.click()
