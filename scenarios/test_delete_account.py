from playwright.sync_api import expect

from pages.account_result.account_result_page import AccountResultPage
from pages.home.home_page import HomePage
from pages.login.login_page import LoginPage


def test_delete_account(page, test_account):
    """DEL-001 회원 탈퇴"""
    home = HomePage(page)
    login_page = LoginPage(page)
    result_page = AccountResultPage(page)

    login_page.open()
    login_page.login(test_account["email"], test_account["password"])
    home.delete_account()

    expect(result_page.account_deleted).to_have_text("Account Deleted!", ignore_case=True)

    # 탈퇴한 계정으로 다시 로그인하면 실패해야 함
    login_page.open()
    login_page.login(test_account["email"], test_account["password"])

    expect(login_page.login_error).to_have_text("Your email or password is incorrect!")
