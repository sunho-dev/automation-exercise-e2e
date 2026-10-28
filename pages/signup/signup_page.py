class SignupPage:
    """계정 정보 입력 화면 (/signup). 로그인 화면에서 이름·이메일을 넣고 Signup을 누르면 나온다."""

    def __init__(self, page):
        self.page = page
        self.gender_mr = page.locator("#id_gender1")
        self.password_input = page.locator("[data-qa='password']")
        self.first_name_input = page.locator("[data-qa='first_name']")
        self.last_name_input = page.locator("[data-qa='last_name']")
        self.address_input = page.locator("[data-qa='address']")
        self.country_select = page.locator("[data-qa='country']")
        self.state_input = page.locator("[data-qa='state']")
        self.city_input = page.locator("[data-qa='city']")
        self.zipcode_input = page.locator("[data-qa='zipcode']")
        self.mobile_number_input = page.locator("[data-qa='mobile_number']")
        self.create_account_button = page.locator("[data-qa='create-account']")

    def fill_account_info(self, account):
        self.gender_mr.check()
        self.password_input.fill(account["password"])
        self.first_name_input.fill(account["first_name"])
        self.last_name_input.fill(account["last_name"])
        self.address_input.fill(account["address"])
        self.country_select.select_option(account["country"])
        self.state_input.fill(account["state"])
        self.city_input.fill(account["city"])
        self.zipcode_input.fill(account["zipcode"])
        self.mobile_number_input.fill(account["mobile_number"])

    def create_account(self):
        self.create_account_button.click()
