# Sonar Demo – Mini Shop (Python)

## 1. Run locally
```
pip install -r requirements.txt
python -m pytest --cov=src --cov-report=xml --cov-report=term
```
This creates `coverage.xml` (starting coverage is about 58%).

Sonar properties you will need later (when you connect the project):
```
sonar.sources=src
sonar.tests=tests
sonar.python.coverage.reportPaths=coverage.xml
```

## 2. What is planted (and where)
| # | File : line | Issue | Category |
|---|-------------|-------|----------|
| 1 | calculator.py:22 | `price > 0 and price > 0` identical operands (S1764) | Reliability (bug) |
| 2 | calculator.py:27 | Mutable default argument `cart=[]` (S5717) | Reliability (bug) |
| 3 | calculator.py:17 | Bare `except:` (S5754) | Reliability / Maintainability |
| 4 | calculator.py:32 | Unused parameter `country` (S1172) | Maintainability |
| 5 | calculator.py:33 | Unused local variable `unused_total` (S1481) | Maintainability |
| 6 | calculator.py:34 | Commented-out code (S125) | Maintainability |
| 7 | calculator.py:35 | TODO comment (S1135) | Maintainability |
| 8 | calculator.py:41-45 | String "Value must be positive" repeated 3 times (S1192) | Maintainability |
| 9 | calculator.py:49 | `shipping_cost` too complex (S3776) | Maintainability |
| 10 | user_service.py:7 | Hard-coded password (S2068/S6418) | Security |
| 11 | user_service.py:11 | MD5 weak hash (S4790) | Security hotspot |
| 12 | user_service.py:15 | `random` used for token (S2245) | Security hotspot |
| 13 | user_service.py:19 | `os.system` with input (S4721) | Security hotspot |
| 14 | user_service.py:24-25 | SSL verification disabled (S4830/S5527) | Security |
| 15 | report.py | `sales_report` / `purchase_report` copy-pasted | Duplication |
| 16 | whole project | Many functions untested | Coverage (~58%) |

Note: exact rule IDs, categories and counts can differ slightly by SonarCloud version and quality profile. Trust your dashboard; this table is the plan.

## 3. How to fix (copy-paste)

### Fix 1 – identical operands (calculator.py)
Replace `if price > 0 and price > 0:` with:
```
    if price > 0:
```

### Fix 2 – mutable default (calculator.py)
```
def add_to_cart(item, cart=None):
    if cart is None:
        cart = []
    cart.append(item)
    return cart
```

### Fix 3 – bare except (calculator.py)
```
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
```

### Fix 4, 5, 6, 7 – calculate_tax (calculator.py)
Replace the whole function with:
```
def calculate_tax(amount, rate):
    return amount * rate
```
(removes the unused parameter, unused variable, commented-out code and the TODO).

### Fix 8 – repeated string (calculator.py)
Add above `validate_order`:
```
ERROR_NEGATIVE = "Value must be positive"
```
Then change all three lines to `raise ValueError(ERROR_NEGATIVE)`.

### Fix 9 – complexity (calculator.py)
Replace the whole `shipping_cost` function with:
```
def _base_cost(weight):
    if weight < 5:
        return 5
    if weight < 20:
        return 10
    return 20


def _express_multiplier(express, international):
    if not express:
        return 1
    return 3 if international else 2


def _fragile_fee(fragile, international):
    if not fragile:
        return 0
    return 15 if international else 5


def shipping_cost(weight, express, international, fragile):
    if weight <= 0:
        return 0
    cost = _base_cost(weight) * _express_multiplier(express, international)
    return cost + _fragile_fee(fragile, international)
```
Existing tests still pass.

### Fix 10 – hard-coded password (user_service.py)
Replace line 7 with:
```
DB_PASSWORD = os.environ.get("DB_PASSWORD")
```
(`os` is already imported.)

### Fix 11 – MD5 (user_service.py)
```
    return hashlib.sha256(password.encode()).hexdigest()
```

### Fix 12 – random token (user_service.py)
Change the import `import random` to `import secrets`, then:
```
def generate_token():
    return str(secrets.randbelow(900000) + 100000)
```

### Fix 13 – os.system (user_service.py)
Change the import to add `import subprocess`, then:
```
def run_report(filename):
    subprocess.run(["cat", filename], check=True)
```
(You can then remove `import os` only if you did not use it in Fix 10.)

### Fix 14 – SSL (user_service.py)
Delete these two lines:
```
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
```

### Fix 15 – duplication (report.py)
Replace the whole file with:
```
"""Text reports for sales and purchases."""


def _build_lines(items):
    lines = []
    total = 0
    for item in items:
        line_total = item["price"] * item["qty"]
        total = total + line_total
        lines.append(item["name"] + " x" + str(item["qty"]) + " = " + str(line_total))
    lines.append("TOTAL: " + str(total))
    lines.append("ITEMS: " + str(len(items)))
    return "\n".join(lines)


def sales_report(items):
    return "SALES REPORT\n" + _build_lines(items)


def purchase_report(items):
    return "PURCHASE REPORT\n" + _build_lines(items)
```

### Fix 16 – coverage (add tests)
Append to `tests/test_calculator.py` (add `safe_divide, calculate_tax, validate_order` to the import line first; if you did Fix 4, call `calculate_tax(100, 0.1)`):
```
def test_safe_divide():
    assert safe_divide(4, 2) == 2
    assert safe_divide(1, 0) is None


def test_calculate_tax():
    assert calculate_tax(100, 0.1) == 10


def test_validate_order():
    assert validate_order(1, 1, 0) is True
    with pytest.raises(ValueError):
        validate_order(-1, 1, 0)
    with pytest.raises(ValueError):
        validate_order(1, -1, 0)
    with pytest.raises(ValueError):
        validate_order(1, 1, -1)
```
Append to `tests/test_report.py` (change import to `from src.report import sales_report, purchase_report`):
```
def test_purchase_report():
    assert "PURCHASE REPORT" in purchase_report(ITEMS)
```
Append to `tests/test_user_service.py` (import `generate_token`):
```
def test_generate_token_length():
    assert len(generate_token()) == 6
```
Then re-run `python -m pytest --cov=src --cov-report=xml` and commit/push `coverage.xml`; coverage jumps to ~90%.

## 4. Suggested demo order
1. Show dashboard: security, reliability, maintainability, duplications, coverage, quality gate failed.
2. Fix security (10-14), then bugs (1-3): show the rating improve.
3. Fix smells (4-9), then duplication (15), then add tests (16): quality gate passes.
