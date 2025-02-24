# ui/dashboard.py
import tkinter as tk
from tkinter import messagebox
from database.inventory_db import Database
from ui.registration import RegistrationWindow
from ui.inventory_ui import InventoryDashboard
from reports.sales_report import SalesReport
from helper import center_window

class AdminDashboard:
    def __init__(self, main_window, login_window_instance):
        self.db = Database()
        self.inventory_dashboard = None  # Add this line to store the InventoryDashboard instance
        self.main_window = main_window
        self.login_window_instance = login_window_instance
        self.root = tk.Toplevel(self.main_window)
        self.root.title("Admin Dashboard")
        self.root.geometry("800x600")
        center_window(self.root)

        # Create the sidebar frame
        self.sidebar = tk.Frame(self.root, bg="#2C3E50", width=150)
        self.sidebar.pack(side="left", fill="y")

        # Create the main content area frame
        self.content_area = tk.Frame(self.root, bg="white")
        self.content_area.pack(side="right", expand=True, fill="both")

        # Add buttons to the sidebar
        self.add_sidebar_button("User Management", self.show_user_management)
        self.add_sidebar_button("Inventory Management", self.open_inventory_management)
        self.add_sidebar_button("Sales Reports", self.show_sales_reports)
        
        # Logout button at the bottom of the sidebar
        logout_button = tk.Button(self.sidebar, text="Logout", command=self.logout, bg="#E74C3C", fg="white", relief="flat")
        logout_button.pack(side="bottom", fill="x", padx=10, pady=10)

    def add_sidebar_button(self, text, command):
        """Helper function to add buttons to the sidebar."""
        button = tk.Button(self.sidebar, text=text, command=command, bg="#34495E", fg="white", relief="flat", height=2)
        button.pack(fill="x", padx=10, pady=5)

    def show_user_management(self):
        # Clear the content area
        self.clear_content_area()
        
        # Add content for User Management
        label = tk.Label(self.content_area, text="User Management", font=("Arial", 16), bg="white")
        label.pack(pady=20)
        
        register_button = tk.Button(self.content_area, text="Register New User", command=self.open_registration_window, bg="green",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=10)
        register_button.pack(pady=10)

    def show_inventory_management(self):
        # Clear the content area
        self.clear_content_area()

        # Add content for Inventory Management
        label = tk.Label(self.content_area, text="Inventory Management", font=("Arial", 16), bg="white")
        label.pack(pady=20)
        
        manage_button = tk.Button(self.content_area, text="Manage Inventory", command=self.open_inventory_management)
        manage_button.pack(pady=10)

    def show_sales_reports(self):
        # Clear the content area
        self.clear_content_area()

        # Add content for Sales Reports
        label = tk.Label(self.content_area, text="Sales Reports", font=("Arial", 16), bg="white")
        label.pack(pady=20)
        
        view_button = tk.Button(self.content_area, text="View Sales Reports", bg="Cyan", command=self.view_sales_reports, font=("Arial", 14, "bold"), padx=10)
        view_button.pack(pady=10)

    def open_registration_window(self):
        RegistrationWindow()

    def open_inventory_management(self):
        self.clear_content_area()

        # If InventoryDashboard is not created, create and display it
        if not self.inventory_dashboard:
            self.inventory_dashboard = InventoryDashboard(self.content_area, "Admin")
        else:
            # Show the inventory dashboard again if it was previously created
            self.inventory_dashboard.create_ui()

    def view_sales_reports(self):
        SalesReport(self.main_window, "Admin")

    def logout(self):
        self.db.close()
        self.root.destroy()
        self.main_window.deiconify()
        self.login_window_instance.show()

    def clear_content_area(self):
        """Remove all widgets from the content area."""
        for widget in self.content_area.winfo_children():
            widget.destroy()


class CashierDashboard:
    def __init__(self, main_window, login_window_instance):
        self.db = Database()
        self.main_window = main_window
        self.inventory_dashboard = None
        self.login_window_instance = login_window_instance
        self.root = tk.Toplevel(self.main_window)
        self.root.title("Cashier Dashboard")
        self.root.geometry("800x600")
        center_window(self.root)

        # Create the sidebar frame
        self.sidebar = tk.Frame(self.root, bg="#2C3E50", width=150)
        self.sidebar.pack(side="left", fill="y")

        # Create the main content area frame
        self.content_area = tk.Frame(self.root, bg="white")
        self.content_area.pack(side="right", expand=True, fill="both")

        # Add buttons to the sidebar
        self.add_sidebar_button("Inventory Management", self.open_inventory_management)
        self.add_sidebar_button("Sales Reports", self.show_sales_reports)
        
        # Logout button at the bottom of the sidebar
        logout_button = tk.Button(self.sidebar, text="Logout", command=self.logout, bg="#E74C3C", fg="white", relief="flat")
        logout_button.pack(side="bottom", fill="x", padx=10, pady=10)

    def add_sidebar_button(self, text, command):
        """Helper function to add buttons to the sidebar."""
        button = tk.Button(self.sidebar, text=text, command=command, bg="#34495E", fg="white", relief="flat", height=2)
        button.pack(fill="x", padx=10, pady=5)

    def show_inventory_management(self):
        # Clear the content area
        self.clear_content_area()

        # Add content for Inventory Management
        label = tk.Label(self.content_area, text="Inventory Management", font=("Arial", 16), bg="white")
        label.pack(pady=20)
        
        manage_button = tk.Button(self.content_area, text="Manage Inventory", command=self.open_inventory_management)
        manage_button.pack(pady=10)

    def show_sales_reports(self):
        # Clear the content area
        self.clear_content_area()

        # Add content for Sales Reports
        label = tk.Label(self.content_area, text="Sales Reports", font=("Arial", 16), bg="white")
        label.pack(pady=20)
        
        view_button = tk.Button(self.content_area, text="View Sales Reports", bg="Cyan", command=self.view_sales_reports, font=("Arial", 14, "bold"), padx=10)
        view_button.pack(pady=10)

    def view_sales_reports(self):
        SalesReport(self.main_window, "Cashier")

    def open_inventory_management(self):
        self.clear_content_area()

        # If InventoryDashboard is not created, create and display it
        if not self.inventory_dashboard:
            self.inventory_dashboard = InventoryDashboard(self.content_area, "Cashier")
        else:
            # Show the inventory dashboard again if it was previously created
            self.inventory_dashboard.create_ui()

    def view_sales_report(self):
        # Open the Sales Report module
        SalesReport(self.main_window, "Cashier")

    def logout(self):
        self.db.close()
        self.root.destroy()
        self.main_window.deiconify()  # Show the main (login) window
        self.login_window_instance.show()  # Reopen login window

    def clear_content_area(self):
        """Remove all widgets from the content area."""
        for widget in self.content_area.winfo_children():
            widget.destroy()