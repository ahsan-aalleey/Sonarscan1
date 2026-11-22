import pytest

from src.calculator import add, divide, apply_discount, add_to_cart, shipping_cost


def test_add():
    assert add(2, 3) == 5


def test_divide():
    assert divide(10, 2) == 5


def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(1, 0)


def test_apply_discount():
    assert apply_discount(100, 10) == 90


def test_add_to_cart():
    assert add_to_cart("pen", []) == ["pen"]


def test_shipping_basic():
    assert shipping_cost(2, False, False, False) == 5
    assert shipping_cost(10, True, False, False) == 20
