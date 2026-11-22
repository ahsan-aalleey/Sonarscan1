"""Text reports for sales and purchases."""


def sales_report(items):
    lines = []
    total = 0
    for item in items:
        name = item["name"]
        price = item["price"]
        qty = item["qty"]
        line_total = price * qty
        total = total + line_total
        lines.append(name + " x" + str(qty) + " = " + str(line_total))
    lines.append("TOTAL: " + str(total))
    lines.append("ITEMS: " + str(len(items)))
    return "SALES REPORT\n" + "\n".join(lines)


def purchase_report(items):
    lines = []
    total = 0
    for item in items:
        name = item["name"]
        price = item["price"]
        qty = item["qty"]
        line_total = price * qty
        total = total + line_total
        lines.append(name + " x" + str(qty) + " = " + str(line_total))
    lines.append("TOTAL: " + str(total))
    lines.append("ITEMS: " + str(len(items)))
    return "PURCHASE REPORT\n" + "\n".join(lines)
