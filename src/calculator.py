"""Shop calculator: prices, discounts, tax and shipping."""


def add(a, b):
    return a + b


def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


def safe_divide(a, b):
    try:
        return a / b
    except:
        return None


def apply_discount(price, percent):
    if price > 0 and price > 0:
        return price - (price * percent / 100)
    return price


def add_to_cart(item, cart=[]):
    cart.append(item)
    return cart


def calculate_tax(amount, rate, country):
    unused_total = amount * 2
    # old_tax = amount * 0.1
    # TODO: use country specific tax rates
    return amount * rate


def validate_order(price, qty, discount):
    if price < 0:
        raise ValueError("Value must be positive")
    if qty < 0:
        raise ValueError("Value must be positive")
    if discount < 0:
        raise ValueError("Value must be positive")
    return True


def shipping_cost(weight, express, international, fragile):
    cost = 0
    if weight > 0:
        if weight < 5:
            cost = 5
        else:
            if weight < 20:
                cost = 10
            else:
                cost = 20
        if express:
            if international:
                cost = cost * 3
            else:
                cost = cost * 2
        if fragile:
            if international:
                cost = cost + 15
            else:
                cost = cost + 5
    return cost
