from playwright.sync_api import expect

from pages.account_result.account_result_page import AccountResultPage
from pages.home.home_page import HomePage
from pages.login.login_page import LoginPage
from pages.signup.signup_page import SignupPage


def test_signup_success(page, new_account):
    """SGN-001 정상 정보로 회원가입"""
    home = HomePage(page)
    login_page = LoginPage(page)
    signup_page = SignupPage(page)
    result_page = AccountResultPage(page)

    home.open()
    home.go_to_signup_login()
    login_page.start_signup(new_account["name"], new_account["email"])
    signup_page.fill_account_info(new_account)
    signup_page.create_account()

    expect(result_page.account_created).to_have_text("Account Created!", ignore_case=True)

    result_page.continue_()

    expect(home.logged_in_as).to_contain_text(new_account["name"])


def test_signup_existing_email(page, test_account):
    """SGN-002 이미 가입된 이메일로 가입 시도"""
    login_page = LoginPage(page)

    login_page.open()
    login_page.start_signup(test_account["name"], test_account["email"])

    expect(login_page.signup_error).to_have_text("Email Address already exist!")
    # 주소는 /signup으로 바뀌지만, 계정 정보 입력 화면이 아니라 같은 가입 폼이 오류와 함께 다시 보인다
    expect(page).to_have_url("/signup")
    expect(login_page.signup_button).to_be_visible()
