import time

import pytest

# 광고가 화면을 가리거나 로딩을 늦추지 않도록 막을 도메인
AD_DOMAINS = ["googlesyndication", "doubleclick", "googleads", "adservice", "fundingchoices"]


@pytest.fixture(autouse=True)
def block_ads(context):
    """모든 시나리오에서 광고 요청을 차단한다."""
    def handle(route):
        if any(domain in route.request.url for domain in AD_DOMAINS):
            route.abort()
        else:
            route.continue_()

    context.route("**/*", handle)


@pytest.fixture
def api(playwright, base_url):
    """사이트 API 호출용. 테스트 계정을 화면 없이 빠르게 만들고 지울 때 사용."""
    request = playwright.request.new_context(base_url=base_url)
    yield request
    request.dispose()


def build_account():
    """매번 겹치지 않는 이메일로 가입 정보를 만든다."""
    return {
        "name": "qa tester",
        "email": f"qa{int(time.time() * 1000)}@example.com",
        "password": "Test1234!",
        "first_name": "qa",
        "last_name": "tester",
        "address": "123 Test St",
        "country": "Canada",
        "state": "Ontario",
        "city": "Toronto",
        "zipcode": "12345",
        "mobile_number": "01012345678",
    }


def delete_account(api, account):
    # 시나리오 안에서 이미 탈퇴했을 수도 있으므로 결과는 확인하지 않는다
    api.delete("/api/deleteAccount", form={"email": account["email"], "password": account["password"]})


@pytest.fixture
def new_account(api):
    """아직 가입하지 않은 계정 정보. 시나리오에서 화면으로 가입하고, 끝나면 탈퇴시킨다."""
    account = build_account()
    yield account
    delete_account(api, account)


@pytest.fixture
def test_account(api):
    """시나리오 시작 전 API로 새 계정을 만들고, 끝나면 탈퇴시킨다."""
    account = build_account()
    response = api.post("/api/createAccount", form={
        "name": account["name"], "email": account["email"], "password": account["password"],
        "title": "Mr", "birth_date": "1", "birth_month": "1", "birth_year": "1995",
        "firstname": account["first_name"], "lastname": account["last_name"], "company": "qa",
        "address1": account["address"], "address2": "", "country": account["country"],
        "zipcode": account["zipcode"], "state": account["state"], "city": account["city"],
        "mobile_number": account["mobile_number"],
    })
    assert response.json()["responseCode"] == 201, response.text()

    yield account

    delete_account(api, account)


@pytest.fixture
def card():
    """결제 화면에 넣을 가짜 카드 정보."""
    return {"name": "qa tester", "number": "4111111111111111", "cvc": "123", "month": "12", "year": "2030"}
