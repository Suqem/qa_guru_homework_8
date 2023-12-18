"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product_book():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_pencil():
    return Product("pencil", 30, "This is a pencil", 350)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product_book):
        # TODO напишите проверки на метод check_quantity
        assert product_book.check_quantity(999)
        assert product_book.check_quantity(1000)
        assert not product_book.check_quantity(2000)

    def test_product_buy(self, product_book):
        # TODO напишите проверки на метод buy
        product_book.buy(500)
        assert product_book.quantity == 500

    def test_product_buy_more_than_available(self, product_book):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product_book.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product_book):
        cart.add_product(product_book, 10)
        assert cart.products[product_book] == 10
        cart.add_product(product_book, 5)
        assert cart.products[product_book] == 15

    def test_add_product_zero_count(self, cart, product_book):
        with pytest.raises(ValueError):
            cart.add_product(product_book, 0)

    def test_remove_product_partial_position(self, cart, product_book):
        cart.add_product(product_book, 20)
        cart.remove_product(product_book, 5)
        assert cart.products[product_book] == 15

    def test_remove_product_whole_position(self, cart, product_book):
        cart.add_product(product_book, 10)
        cart.remove_product(product_book)
        assert product_book not in cart.products

    def test_remove_product_whole_position_v2(self, cart, product_book):
        cart.add_product(product_book, 10)
        cart.remove_product(product_book, 10)
        assert len(cart.products) == 0

    def test_remove_product_greater_than_position(self, cart, product_book):
        cart.add_product(product_book, 5)
        cart.remove_product(product_book, 10)
        assert product_book not in cart.products

    def test_clear_one_product(self, cart, product_book):
        cart.add_product(product_book, 5)
        cart.clear()
        assert len(cart.products) == 0

    def test_clear_two_product(self, cart, product_book, product_pencil):
        cart.add_product(product_book, 5)
        cart.add_product(product_pencil, 10)
        cart.clear()
        assert len(cart.products) == 0

    def test_get_total_price_empty_cart(self, cart):
        assert cart.get_total_price() == 0

    def test_get_total_price_single_product(self, cart, product_book):
        cart.add_product(product_book, 5)
        assert cart.get_total_price() == 500

    def test_get_total_price_multiple_products(self, cart, product_book, product_pencil):
        cart.add_product(product_book, 5)
        cart.add_product(product_pencil, 10)
        assert cart.get_total_price() == 800

    def test_buy_sufficient_stock(self, cart, product_book):
        cart.add_product(product_book, 100)
        cart.buy()
        assert len(cart.products) == 0
        assert product_book.quantity == 900

    def test_buy_insufficient_stock(self, cart, product_book):
        cart.add_product(product_book, 10000)
        with pytest.raises(ValueError):
            cart.buy()

    def test_buy_empty_cart(self, cart):
        with pytest.raises(ValueError):
            cart.buy()
