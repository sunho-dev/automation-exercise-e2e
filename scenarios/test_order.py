from playwright.sync_api import expect

from pages.account_result.account_result_page import AccountResultPage
from pages.cart.cart_page import CartPage
from pages.checkout.checkout_page import CheckoutPage
from pages.home.home_page import HomePage
from pages.login.login_page import LoginPage
from pages.payment.payment_page import PaymentPage
from pages.product_detail.product_detail_page import ProductDetailPage
from pages.products.products_page import ProductsPage
from pages.signup.signup_page import SignupPage


def test_order_logged_in(page, test_account, card):
    """ORD-001 로그인 후 주문"""
    login_page = LoginPage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    payment_page = PaymentPage(page)

    login_page.open()
    login_page.login(test_account["email"], test_account["password"])
    products_page.open()
    products_page.add_to_cart(0)
    products_page.view_cart()
    cart_page.proceed_to_checkout()
    checkout_page.place_order()
    payment_page.pay(card)

    expect(payment_page.order_placed).to_have_text("Order Placed!", ignore_case=True)
    expect(payment_page.order_confirmed_message).to_be_visible()


def test_order_guest_signup_at_checkout(page, new_account, card):
    """ORD-002 비로그인 주문 (결제 단계에서 회원가입)"""
    home = HomePage(page)
    login_page = LoginPage(page)
    signup_page = SignupPage(page)
    result_page = AccountResultPage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    payment_page = PaymentPage(page)

    # 1~2. 로그인 없이 상품을 담고 결제 시도
    products_page.open()
    product_name = products_page.get_product_name(0)
    products_page.add_to_cart(0)
    products_page.view_cart()
    cart_page.proceed_to_checkout()

    expect(cart_page.checkout_modal).to_contain_text("Register / Login account to proceed on checkout.")

    # 3. 팝업에서 회원가입
    cart_page.go_to_register_login()
    login_page.start_signup(new_account["name"], new_account["email"])
    signup_page.fill_account_info(new_account)
    signup_page.create_account()
    result_page.continue_()

    # 4. 가입 전에 담은 상품이 그대로 있는지
    home.go_to_cart()
    expect(cart_page.row(product_name)).to_be_visible()

    # 5. 주문
    cart_page.proceed_to_checkout()
    checkout_page.place_order()
    payment_page.pay(card)

    expect(payment_page.order_placed).to_have_text("Order Placed!", ignore_case=True)

    # 6. 탈퇴
    home.delete_account()

    expect(result_page.account_deleted).to_have_text("Account Deleted!", ignore_case=True)


def test_order_multiple_items(page, test_account, card):
    """ORD-003 장바구니 주문 (여러 상품·수량)"""
    login_page = LoginPage(page)
    detail_page = ProductDetailPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)
    payment_page = PaymentPage(page)

    login_page.open()
    login_page.login(test_account["email"], test_account["password"])

    # 1. 서로 다른 상품 2개 담기 (하나는 수량 2)
    quantities = {}
    for product_id, quantity in [(1, 1), (2, 2)]:
        detail_page.open(product_id)
        quantities[detail_page.get_product_name()] = quantity
        detail_page.add_to_cart(quantity)
        detail_page.continue_shopping()

    # 2. 상품별 합계 = 가격 × 수량
    cart_page.open()
    expected_total = 0
    for name, quantity in quantities.items():
        item = cart_page.get_item(name)
        assert item["quantity"] == quantity
        assert item["total"] == item["price"] * quantity
        expected_total += item["total"]

    # 3. Total Amount = 상품별 합계의 합
    cart_page.proceed_to_checkout()
    assert checkout_page.get_total_amount() == expected_total

    # 4. 결제
    checkout_page.place_order()
    payment_page.pay(card)

    expect(payment_page.order_placed).to_have_text("Order Placed!", ignore_case=True)


def test_checkout_delivery_address(page, test_account):
    """ORD-004 주문 확인 화면의 배송지 확인"""
    login_page = LoginPage(page)
    products_page = ProductsPage(page)
    cart_page = CartPage(page)
    checkout_page = CheckoutPage(page)

    login_page.open()
    login_page.login(test_account["email"], test_account["password"])
    products_page.open()
    products_page.add_to_cart(0)
    products_page.view_cart()
    cart_page.proceed_to_checkout()

    # 배송지가 가입할 때 넣은 정보와 같은지
    for key in ["first_name", "last_name", "address", "city", "state", "zipcode", "country", "mobile_number"]:
        expect(checkout_page.delivery_address).to_contain_text(test_account[key])
