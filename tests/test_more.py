import pytest

from src import user_service
from src.calculator import (
    safe_divide, apply_discount, calculate_tax, validate_order, shipping_cost,
)
from src.report import purchase_report
from src.user_service import generate_token, run_report, make_ssl_context


# ---- calculator ----
def test_safe_divide():
    assert safe_divide(4, 2) == 2
    assert safe_divide(1, 0) is None


def test_apply_discount_non_positive_price():
    assert apply_discount(0, 10) == 0
    assert apply_discount(-5, 10) == -5


def test_calculate_tax():
    assert calculate_tax(100, 0.1, "US") == pytest.approx(10)


def test_validate_order_ok():
    assert validate_order(1, 1, 1) is True


@pytest.mark.parametrize("args", [(-1, 1, 1), (1, -1, 1), (1, 1, -1)])
def test_validate_order_negative(args):
    with pytest.raises(ValueError):
        validate_order(*args)


def test_shipping_cost_branches():
    assert shipping_cost(0, False, False, False) == 0
    assert shipping_cost(10, False, False, False) == 10
    assert shipping_cost(25, False, False, False) == 20
    assert shipping_cost(2, True, True, False) == 15
    assert shipping_cost(2, True, False, False) == 10
    assert shipping_cost(2, False, False, True) == 10
    assert shipping_cost(2, False, True, True) == 20


# ---- report ----
def test_purchase_report():
    items = [{"name": "pen", "price": 2, "qty": 3}]
    result = purchase_report(items)
    assert "PURCHASE REPORT" in result
    assert "TOTAL: 6" in result


# ---- user_service ----
def test_generate_token():
    token = generate_token()
    assert len(token) == 6 and token.isdigit()


def test_run_report(monkeypatch):
    calls = []
    monkeypatch.setattr(user_service.os, "system", lambda cmd: calls.append(cmd))
    run_report("file.txt")
    assert calls == ["cat file.txt"]


def test_make_ssl_context():
    ctx = make_ssl_context()
    assert ctx.check_hostname is False