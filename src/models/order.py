# order.py
class Order:
    def __init__(self, order_total, total_items, order_date):
        self.order_total = order_total  # Total price of the order
        self.total_items = total_items  # Number of items in the order
        self.order_date = order_date    # Date when the order was placed

    def __str__(self):
        return f"Order(Date: {self.order_date}, Items: {self.total_items}, Total: ${self.order_total:.2f})"
