# sales.py
class Sale:
    def __init__(self, order_id, item_id, item_name, unit_price, quantity, sale_date):
        self.order_id = order_id          # Associated order ID
        self.item_id = item_id            # Item ID being sold
        self.item_name = item_name        # Item name
        self.unit_price = unit_price      # Price per unit
        self.quantity = quantity          # Quantity sold
        self.total_price = unit_price * quantity  # Calculated total price
        self.sale_date = sale_date        # Date of the sale

    def __str__(self):
        return (f"Sale(Item: {self.item_name}, Quantity: {self.quantity}, "
                f"Unit Price: ${self.unit_price:.2f}, Total: ${self.total_price:.2f}, Date: {self.sale_date})")
