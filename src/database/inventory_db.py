# inventory_db.py
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="inventory.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        # Create Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT CHECK(role IN ('Admin', 'Cashier')) NOT NULL
            )
        ''')

        # Create Items table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Items (
                item_id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                price REAL NOT NULL CHECK(price >= 0),
                quantity INTEGER NOT NULL CHECK(quantity >= 0)
            )
        ''')

        #Create Sales table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER,
                item_id INTEGER,
                item_name TEXT,
                unit_price REAL,
                quantity INTEGER,
                total_price REAL,
                sale_date TEXT,
                FOREIGN KEY(order_id) REFERENCES orders(order_id),
                FOREIGN KEY(item_id) REFERENCES items(item_id)
            )
        """)

        #Create Order table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_total REAL,
                total_items INTEGER,
                order_date TEXT
            )
        """)
        self.connection.commit()

        # Check if the Admin user exists; if not, add a default Admin
        self.create_default_admin()

    def create_default_admin(self):
        self.cursor.execute("SELECT * FROM Users WHERE username = 'admin'")
        if not self.cursor.fetchone():  # If no admin found
            self.cursor.execute(
                "INSERT INTO Users (username, password, role) VALUES (?, ?, ?)",
                ('admin', 'password123', 'Admin')
            )
            self.connection.commit()
            print("Default Admin user created with username 'admin' and password 'password123'.")

    def add_user(self, username, password, role):
        self.cursor.execute("INSERT INTO Users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        self.connection.commit()

    def get_user(self, username):
        self.cursor.execute("SELECT * FROM Users WHERE username = ?", (username,))
        return self.cursor.fetchone()

    def add_item(self, name, price, quantity):
        self.cursor.execute("INSERT INTO Items (name, price, quantity) VALUES (?, ?, ?)", (name, price, quantity))
        self.connection.commit()

    def item_exists(self, name):
        """Check if an item with the given name already exists in the database."""
        self.cursor.execute("SELECT 1 FROM Items WHERE name = ?", (name,))
        return self.cursor.fetchone() is not None

    def update_item_quantity(self, item_id, quantity):
        self.cursor.execute("UPDATE Items SET quantity = ? WHERE item_id = ?", (quantity, item_id))
        self.connection.commit()

    def delete_item(self, item_id):
        self.cursor.execute("DELETE FROM Items WHERE item_id = ?", (item_id,))
        self.connection.commit()

    def update_item(self, item_id, name, price, quantity):
        self.cursor.execute(
            "UPDATE Items SET name = ?, price = ?, quantity = ? WHERE item_id = ?",
            (name, price, quantity, item_id)
        )
        self.connection.commit()

    def fetch_item(self, item_id):
        self.cursor.execute("SELECT * FROM Items WHERE item_id = ?", (item_id,))
        return self.cursor.fetchone()

    def fetch_all_items(self):
        self.cursor.execute("SELECT * FROM Items")
        return self.cursor.fetchall()

    def add_order(self, order_total, total_items):
        """Add a new order record to the orders table."""
        cursor = self.connection.cursor()
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO orders (order_total, total_items, order_date)
            VALUES (?, ?, ?)
        """, (order_total, total_items, order_date))
        self.connection.commit()
        return cursor.lastrowid  # Return the new order ID

    def add_sale(self, order_id, item_id, item_name, unit_price, quantity):
        """Add a new sale record to the sales table."""
        cursor = self.connection.cursor()
        total_price = unit_price * quantity
        sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Current date and time
        cursor.execute("""
            INSERT INTO sales (order_id, item_id, item_name, unit_price, quantity, total_price, sale_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (order_id, item_id, item_name, unit_price, quantity, total_price, sale_date))
        self.connection.commit()

    def update_item_stock(self, item_id, quantity_change):
        """Update the stock quantity of an item."""
        cursor = self.connection.cursor()
        cursor.execute("UPDATE items SET quantity = quantity + ? WHERE item_id = ?", (quantity_change, item_id))
        self.connection.commit()

    def get_sales_between_dates(self, start_date, end_date):
        """Retrieve sales data between two dates (inclusive)."""
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM sales
            WHERE sale_date BETWEEN ? AND ?
            ORDER BY sale_date ASC
        """, (start_date.strftime("%Y-%m-%d 00:00:00"), end_date.strftime("%Y-%m-%d 23:59:59")))
        return cursor.fetchall()


    def close(self):
        self.connection.close()
