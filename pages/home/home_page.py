class HomePage:
    """모든 화면 상단에 있는 메뉴 영역."""

    def __init__(self, page):
        self.page = page
        self.signup_login_menu = page.locator("a[href='/login']")
        self.cart_menu = page.locator("header a[href='/view_cart']")
        self.logout_menu = page.locator("a[href='/logout']")
        self.delete_account_menu = page.locator("a[href='/delete_account']")
        self.logged_in_as = page.locator("li", has_text="Logged in as")

    def open(self):
        self.page.goto("/")

    def go_to_signup_login(self):
        self.signup_login_menu.click()

    def go_to_cart(self):
        self.cart_menu.click()

    def logout(self):
        self.logout_menu.click()

    def delete_account(self):
        self.delete_account_menu.click()
