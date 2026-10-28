from playwright.sync_api import expect

from pages.cart.cart_page import CartPage
from pages.product_detail.product_detail_page import ProductDetailPage
from pages.products.products_page import ProductsPage


def test_add_to_cart(page):
    """CRT-001 상품을 장바구니에 담기"""
    products_page = ProductsPage(page)
    cart_page = CartPage(page)

    products_page.open()
    product_name = products_page.get_product_name(0)
    products_page.add_to_cart(0)
    products_page.view_cart()

    expect(cart_page.row(product_name)).to_be_visible()
    item = cart_page.get_item(product_name)
    assert item["quantity"] == 1
    assert item["total"] == item["price"]


def test_add_to_cart_with_quantity(page):
    """CRT-002 상품 상세에서 수량 지정 후 담기"""
    detail_page = ProductDetailPage(page)
    cart_page = CartPage(page)

    detail_page.open(1)
    product_name = detail_page.get_product_name()
    detail_page.add_to_cart(4)
    cart_page.open()

    item = cart_page.get_item(product_name)
    assert item["quantity"] == 4
    assert item["total"] == item["price"] * 4


def test_delete_from_cart(page):
    """CRT-003 장바구니에서 상품 삭제"""
    products_page = ProductsPage(page)
    cart_page = CartPage(page)

    products_page.open()
    product_name = products_page.get_product_name(0)
    products_page.add_to_cart(0)
    products_page.view_cart()
    cart_page.delete(product_name)

    expect(cart_page.row(product_name)).to_have_count(0)
    expect(cart_page.empty_cart_message).to_contain_text("Cart is empty!")
