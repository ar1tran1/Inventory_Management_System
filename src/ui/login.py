import tkinter as tk
from tkinter import messagebox
from tkinter import PhotoImage  # For adding the logo
from database.inventory_db import Database
from ui.dashboard import AdminDashboard, CashierDashboard
from helper import center_window

class LoginWindow:
    def __init__(self, root):
        self.db = Database()
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x200")
        center_window(self.root)
        
        # Call setup method to initialize the widgets
        self.setup_widgets()

    def setup_widgets(self):
        # Clear any existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()

        # Add logo at the top
        try:
            logo = PhotoImage(file="./logo.png")  # Replace with the path to your logo file
            self.logo_label = tk.Label(self.root, image=logo)
            self.logo_label.image = logo  # Keep a reference to avoid garbage collection
            self.logo_label.pack(pady=10)
        except Exception as e:
            print(f"Logo could not be loaded: {e}")

        # Add application name in bold
        app_name_label = tk.Label(
            self.root, 
            text="BYTE CART",  # Replace with your application name
            font=("Arial", 16, "bold")
        )
        app_name_label.pack(pady=5)

        # Add username and password fields
        self.username_label = tk.Label(self.root, text="Username", font=("Arial", 12))
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Password", font=("Arial", 12))
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 12), width=30, show="*")
        self.password_entry.pack(pady=5)

        # Login button
        self.login_button = tk.Button(
            self.root,
            text="Login",
            command=self.login,
            bg="green",
            fg="white",
            font=("Arial", 13, "bold"),
            padx=10
        )
        self.login_button.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.db.get_user(username)
        if user and user[2] == password:  # Check if the plain-text password matches
            role = user[3]
            messagebox.showinfo("Login Successful", f"Welcome, {role}")
            self.root.withdraw()  # Hide the main (login) window

            # Open the appropriate dashboard based on the role
            if role == "Admin":
                AdminDashboard(self.root, self)
            elif role == "Cashier":
                CashierDashboard(self.root, self)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def show(self):
        """Show the login window again after logout."""
        self.setup_widgets()  # Reset the widgets in case of any previous login attempt
        self.root.deiconify()
