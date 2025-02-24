# ui/inventory_ui.py
import tkinter as tk
from tkinter import messagebox, ttk
from database.inventory_db import Database
from helper import center_window

class InventoryDashboard:
    def __init__(self, root, role):
        self.db = Database()
        self.role = role
        self.root = root
        self.cart = []
        self.create_ui()

    def create_ui(self):
        # Clear existing content
        for widget in self.root.winfo_children():
            widget.destroy()

        # Layout with items table and cart summary
        self.create_items_table()
        self.create_cart_summary()

    def create_items_table(self):
        # Items list frame
        items_frame = tk.Frame(self.root)
        items_frame.pack(side="left", fill="both", expand=True)

        # Add 'Add Item' button
        add_item_button = tk.Button(items_frame, text="Add Item", command=self.add_item_popup, bg="green",
            fg="white",
            font=("Arial", 12),
            padx=10)
        add_item_button.pack(anchor='ne', padx=10, pady=10)

        # Define columns for items table
        columns = ("Item ID", "Item Name", "Quantity", "Price", "Actions")
        self.tree = ttk.Treeview(items_frame, columns=columns, show="headings")

        # Set up column headers
        for col in columns[:-1]:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=150)

        # Actions column
        self.tree.heading("Actions", text="Actions")
        self.tree.column("Actions", anchor="center", width=200)

        # Populate table with items
        self.populate_items_table()

        # Bind action events
        self.tree.bind("<ButtonRelease-1>", self.handle_actions)
        self.tree.pack(fill="both", expand=True)

        # Quantity label and entry
        quantity_label = tk.Label(items_frame, text="Quantity:", font=("Arial", 16, "bold"))
        quantity_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.quantity_entry = tk.Entry(items_frame, width=10, font=("Arial", 16, "bold"))
        self.quantity_entry.insert(0, "1")  # Default quantity is 1
        self.quantity_entry.pack(anchor="w", padx=10, pady=5)

    def populate_items_table(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Fetch items from the database
        items = self.db.fetch_all_items()
        
        for item in items:
            # Insert item data with actions
            self.tree.insert("", "end", values=(item[0], item[1], item[3], f"${item[2]:.2f}", "Edit || Delete || AddToCart"))

    def handle_actions(self, event):
        """Handle clicks on the 'Actions' column for Edit, Delete, or Add to Cart."""
        item_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if column == '#5':  # Actions column
            item_values = self.tree.item(item_id, 'values')
            if item_values:
                x, y, width, height = self.tree.bbox(item_id, column="#5")
                click_x = event.x - x

                if click_x < width // 3:
                    self.edit_item_popup(item_values[0])  # Edit item
                elif click_x < 1.5 * width // 3:
                    self.delete_item(item_values[0])  # Delete item
                else:
                    self.add_to_cart(item_values)  # Add to cart

    def add_to_cart(self, item_values):
        """Adds an item to the cart and updates the cart summary."""
        item_id, item_name, quantity, price = item_values[:4]
        try:
            selected_quantity = int(self.quantity_entry.get())
            if selected_quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a positive integer.")
            return

        if selected_quantity > int(quantity):
            messagebox.showerror("Error", f"Only {quantity} units available in stock.")
            return

        cart_item = {"Item ID": item_id, "Item Name": item_name, "Quantity": selected_quantity, "Price": price}
        self.cart.append(cart_item)
        self.update_cart_summary()
        messagebox.showinfo("Success", f"Added {selected_quantity} unit(s) of '{item_name}' to cart.")

    def create_cart_summary(self):
        # Adjust the width of the cart frame
        cart_frame = tk.Frame(self.root, bg="lightblue", width=400)  # Increased width from 200 to 300
        cart_frame.pack(side="right", fill="y")

        tk.Label(cart_frame, text="Cart Summary", bg="lightblue", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Listbox for the cart items
        self.cart_listbox = tk.Listbox(cart_frame, width=40)  # Adjusted width for better alignment
        self.cart_listbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.total_label = tk.Label(cart_frame, text="Total: $0.00", bg="lightblue", font=("Arial", 12, "bold"))
        self.total_label.pack(pady=10)

        # Clear Cart button
        clear_cart_button = tk.Button(cart_frame, text="Clear Cart", bg="red", fg="white", font=("Arial", 12, "bold"),
                                    command=self.clear_cart)
        clear_cart_button.pack(pady=5, side="left", padx=20)  

        # Checkout button
        checkout_button = tk.Button(cart_frame, text="Checkout", bg="green", fg="white", font=("Arial", 12, "bold"),
                                    command=self.checkout_cart)
        checkout_button.pack(pady=5, side="right", padx=20)  #


    def clear_cart(self):
        """Clears the cart and updates the cart summary."""
        self.cart = []  # Empty the cart
        self.update_cart_summary()  # Refresh the cart summary
        messagebox.showinfo("Cart Cleared", "All items have been removed from the cart.")



    def checkout_cart(self):
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty. Add items to cart before checkout.")
            return

        # Create a summary popup
        popup = tk.Toplevel(self.root)
        popup.title("Order Summary")
        center_window(popup)

        # Set the main container frame with center alignment
        frame = tk.Frame(popup, padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        # Order Summary Title
        tk.Label(frame, text="Order Summary", font=("Arial", 16), anchor="center").pack(pady=10)

        # Frame for order items with scrollbar
        items_frame = tk.Frame(frame)
        items_frame.pack(pady=10, fill="both", expand=True)

        # Create a canvas for scrolling
        canvas = tk.Canvas(items_frame)
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(items_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        # Add the frame inside the canvas
        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Display order items
        for item in self.cart:
            tk.Label(
                scrollable_frame,
                text=f"{item['Item Name']} x {item['Quantity']} - ${float(item['Price'].replace('$', '')) * item['Quantity']:.2f}",
                font=("Arial", 12)
            ).pack(anchor="w", pady=2)

        # Display total items and total price
        tk.Label(frame, text=f"Total Items: {sum(item['Quantity'] for item in self.cart)}", font=("Arial", 12)).pack(pady=5)
        tk.Label(frame, text=f"Order Total: ${sum(float(item['Price'].replace('$', '')) * item['Quantity'] for item in self.cart):.2f}", font=("Arial", 12)).pack(pady=5)

        # Buttons container
        buttons_frame = tk.Frame(frame, pady=10)
        buttons_frame.pack()

        # Cancel button on the left
        cancel_button = tk.Button(
            buttons_frame,
            text="Cancel",
            command=popup.destroy,
            bg="red",
            fg="white",
            font=("Arial", 12),
            padx=10
        )
        cancel_button.pack(side="left", padx=5)

        # Place Order button on the right
        save_button = tk.Button(
            buttons_frame,
            text="Place Order",
            command=lambda: self.save_order(popup),
            bg="green",
            fg="white",
            font=("Arial", 12),
            padx=10
        )
        save_button.pack(side="left", padx=5)

    def save_order(self, popup):
        """Save the order in the orders and sales tables, and update stock."""
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty. Add items to cart before checkout.")
            return

        try:
            total_items = sum(item["Quantity"] for item in self.cart)
            order_total = sum(float(item["Price"].replace("$", "")) * item["Quantity"] for item in self.cart)

            # Add a new order record
            order_id = self.db.add_order(order_total, total_items)

            # Add sales records and update stock for each cart item
            for item in self.cart:
                item_id = item["Item ID"]
                item_name = item["Item Name"]
                unit_price = float(item["Price"].replace("$", ""))
                quantity = item["Quantity"]

                # Deduct quantity from stock
                self.db.update_item_stock(item_id, -quantity)

                # Save sale record
                self.db.add_sale(order_id, item_id, item_name, unit_price, quantity)

            # Clear the cart
            messagebox.showinfo("Success", f"Order #{order_id} placed successfully!")
            self.cart = []  # Clear the cart
            self.update_cart_summary()
            self.populate_items_table()
            popup.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the order: {e}")

    def update_cart_summary(self):
        """Updates the cart summary with items and total price."""
        self.cart_listbox.delete(0, tk.END)
        total_price = 0.0

        for item in self.cart:
            item_price = float(item["Price"].replace("$", ""))
            total_item_price = item_price * item["Quantity"]
            total_price += total_item_price
            self.cart_listbox.insert(tk.END, f"{item['Item Name']} x {item['Quantity']} - ${total_item_price:.2f}")

        self.total_label.config(text=f"Total: ${total_price:.2f}")

    def add_item_popup(self):
        """Opens a popup for adding a new item if the user role is not 'cashier'."""
        if self.role == 'Cashier':
            messagebox.showerror("Permission Denied", "You do not have permission to add new items.")
            return  # Prevents the popup from opening

        """Opens a popup for adding a new item."""
        popup = tk.Toplevel(self.root)
        popup.title("Add New Item")
        center_window(popup, 400, 300)

        # Configure the grid layout for centering
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_columnconfigure(1, weight=1)
        popup.grid_rowconfigure(5, weight=1)

        # Input fields
        tk.Label(popup, text="Item Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        item_name_entry = tk.Entry(popup)
        item_name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(popup, text="Quantity:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        quantity_entry = tk.Entry(popup)
        quantity_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(popup, text="Price:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        price_entry = tk.Entry(popup)
        price_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        cancel_button = tk.Button(
            popup, 
            text="Cancel", 
            command=popup.destroy, 
            bg="red", 
            fg="white", 
            font=("Arial", 12), 
            padx=10
        )
        cancel_button.grid(row=4, column=0, pady=10, sticky="e")  # Positioned to the left

        add_button = tk.Button(
            popup, 
            text="Save", 
            command=lambda: self.save_new_item(popup, item_name_entry, quantity_entry, price_entry), 
            bg="green", 
            fg="white", 
            font=("Arial", 12), 
            padx=10
        )
        add_button.grid(row=4, column=1, pady=10)  # Positioned to the right


    def save_new_item(self, popup, name_entry, quantity_entry, price_entry):
        """Validates and saves a new item to the database."""
        name = name_entry.get().strip()
        quantity = quantity_entry.get().strip()
        price = price_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Item name is required.")
            return
        if not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Error", "Quantity must be a positive integer.")
            return
        if not price.replace('.', '', 1).isdigit() or float(price) <= 0:
            messagebox.showerror("Error", "Price must be a positive number.")
            return
        if self.db.item_exists(name):
            messagebox.showerror("Error", "An item with this name already exists.")
            return

        self.db.add_item(name, float(price), int(quantity))
        messagebox.showinfo("Success", f"Item '{name}' added successfully.")
        
        self.populate_items_table()
        popup.destroy()

    def edit_item_popup(self, item_id):
        """Opens a popup for editing an existing item."""
        item = self.db.fetch_item(item_id)
        if not item:
            messagebox.showerror("Error", "Item not found.")
            return

        popup = tk.Toplevel(self.root)
        popup.title("Edit Item")
        center_window(popup, 400, 300)

        # Configure the grid layout for centering
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_columnconfigure(1, weight=1)
        popup.grid_rowconfigure(5, weight=1)

        tk.Label(popup, text="Item Name:").grid(row=0, column=0, padx=10, pady=5)
        name_entry = tk.Entry(popup)
        name_entry.insert(0, item[1])
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(popup, text="Quantity:").grid(row=1, column=0, padx=10, pady=5)
        quantity_entry = tk.Entry(popup)
        quantity_entry.insert(0, item[3])
        quantity_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(popup, text="Price:").grid(row=2, column=0, padx=10, pady=5)
        price_entry = tk.Entry(popup)
        price_entry.insert(0, item[2])
        price_entry.grid(row=2, column=1, padx=10, pady=5)

        # Disable fields if the user role is 'cashier'
        if self.role == 'Cashier':
            name_entry.config(state='disabled')
            price_entry.config(state='disabled')


        # Buttons
        cancel_button = tk.Button(
            popup, 
            text="Cancel", 
            command=popup.destroy, 
            bg="red", 
            fg="white", 
            font=("Arial", 12), 
            padx=10
        )
        cancel_button.grid(row=4, column=0, pady=10, sticky="e")  # Positioned to the left

        update_button = tk.Button(popup, text="Update Item", command=lambda: self.update_item(popup, item_id, name_entry, quantity_entry, price_entry), bg="green", 
            fg="white", 
            font=("Arial", 12), 
            padx=10)
        update_button.grid(row=4, column=1, pady=10)


    def update_item(self, popup, item_id, name_entry, quantity_entry, price_entry):
        """Validates and updates an item in the database."""
        name = name_entry.get().strip()
        quantity = quantity_entry.get().strip()
        price = price_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Item name is required.")
            return
        if not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Error", "Quantity must be a positive integer.")
            return
        if not price.replace('.', '', 1).isdigit() or float(price) <= 0:
            messagebox.showerror("Error", "Price must be a positive number.")
            return

        self.db.update_item(item_id, name, float(price), int(quantity))
        messagebox.showinfo("Success", f"Item '{name}' updated successfully.")
        
        self.populate_items_table()
        popup.destroy()

    def delete_item(self, item_id):
        if self.role == 'Cashier':
            messagebox.showerror("Permission Denied", "You do not have permission to delete items.")
            return

        """Deletes an item after confirmation."""
        if messagebox.askyesno("Delete Item", "Are you sure you want to delete this item?"):
            self.db.delete_item(item_id)
            self.populate_items_table()
