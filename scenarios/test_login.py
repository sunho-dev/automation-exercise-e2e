from playwright.sync_api import expect

from pages.home.home_page import HomePage
from pages.login.login_page import LoginPage


def test_login_success(page, test_account):
    """LGN-001 정상 계정으로 로그인"""
    home = HomePage(page)
    login_page = LoginPage(page)

    home.open()
    home.go_to_signup_login()
    login_page.login(test_account["email"], test_account["password"])

    expect(home.logged_in_as).to_contain_text(test_account["name"])
    expect(home.logout_menu).to_be_visible()
    expect(home.delete_account_menu).to_be_visible()


def test_login_wrong_password(page, test_account):
    """LGN-002 잘못된 비밀번호로 로그인"""
    home = HomePage(page)
    login_page = LoginPage(page)

    login_page.open()
    login_page.login(test_account["email"], "wrong-password")

    expect(login_page.login_error).to_have_text("Your email or password is incorrect!")
    expect(home.logged_in_as).to_be_hidden()


def test_logout(page, test_account):
    """LGN-003 로그아웃"""
    home = HomePage(page)
    login_page = LoginPage(page)

    login_page.open()
    login_page.login(test_account["email"], test_account["password"])
    home.logout()

    expect(page).to_have_url("/login")
    expect(home.logged_in_as).to_be_hidden()
