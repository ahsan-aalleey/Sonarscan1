from src.report import sales_report

ITEMS = [{"name": "pen", "price": 2, "qty": 3}]


def test_sales_report():
    result = sales_report(ITEMS)
    assert "SALES REPORT" in result
    assert "TOTAL: 6" in result
