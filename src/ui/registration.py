# ui/registration.py
import tkinter as tk
from tkinter import messagebox
from database.inventory_db import Database
from helper import center_window

class RegistrationWindow:
    def __init__(self):
        self.db = Database()
        self.root = tk.Tk()
        self.root.title("Register New User")
        self.root.geometry("300x200")
        center_window(self.root, 400, 300)

        self.username_label = tk.Label(self.root, text="Username:", font=("Arial", 12))
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Password:", font=("Arial", 12))
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, font=("Arial", 12), width=30, show="*")
        self.password_entry.pack(pady=5)

        self.role_label = tk.Label(self.root, text="Role (Admin/Cashier):", font=("Arial", 12))
        self.role_label.pack(pady=5)
        self.role_entry = tk.Entry(self.root, font=("Arial", 12), width=30)
        self.role_entry.pack(pady=5)

        self.register_button = tk.Button(self.root, text="Register", command=self.register_user, bg="green",
            fg="white",
            font=("Arial", 12),
            padx=10)
        self.register_button.pack()

        self.root.mainloop()

    def register_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()

        if role not in ["Admin", "Cashier"]:
            messagebox.showerror("Error", "Role must be either 'Admin' or 'Cashier'")
            return

        try:
            self.db.add_user(username, password, role)
            messagebox.showinfo("Success", "User registered successfully")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register user: {e}")

    def close(self):
        self.db.close()
