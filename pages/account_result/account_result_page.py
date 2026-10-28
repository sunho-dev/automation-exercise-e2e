class AccountResultPage:
    """가입 완료(/account_created)·탈퇴 완료(/delete_account) 안내 화면."""

    def __init__(self, page):
        self.page = page
        self.account_created = page.locator("[data-qa='account-created']")
        self.account_deleted = page.locator("[data-qa='account-deleted']")
        self.continue_button = page.locator("[data-qa='continue-button']")

    def continue_(self):
        self.continue_button.click()
