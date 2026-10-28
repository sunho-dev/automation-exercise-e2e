class LoginPage:
    """Signup / Login 화면 (/login). 왼쪽은 로그인, 오른쪽은 회원가입 시작 폼."""

    def __init__(self, page):
        self.page = page
        self.login_email_input = page.locator("[data-qa='login-email']")
        self.login_password_input = page.locator("[data-qa='login-password']")
        self.login_button = page.locator("[data-qa='login-button']")
        self.login_error = page.locator("form[action='/login'] p")

        self.signup_name_input = page.locator("[data-qa='signup-name']")
        self.signup_email_input = page.locator("[data-qa='signup-email']")
        self.signup_button = page.locator("[data-qa='signup-button']")
        self.signup_error = page.locator("form[action='/signup'] p")

    def open(self):
        self.page.goto("/login")

    def login(self, email, password):
        self.login_email_input.fill(email)
        self.login_password_input.fill(password)
        self.login_button.click()

    def start_signup(self, name, email):
        self.signup_name_input.fill(name)
        self.signup_email_input.fill(email)
        self.signup_button.click()
