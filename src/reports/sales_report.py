import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar  # Ensure to install tkcalendar: pip install tkcalendar
from datetime import datetime, timedelta
from database.inventory_db import Database  # Adjust as per your actual database import
from helper import center_window

class SalesReport:
    def __init__(self, main_window, role):
        self.db = Database()
        self.main_window = main_window
        self.role = role
        self.root = tk.Toplevel(self.main_window)
        self.root.title(f"{self.role} - Sales Report")
        self.root.geometry("500x400")
        center_window(self.root, 1000, 800)

        # Title Label
        tk.Label(self.root, text="Sales Report", font=("Arial", 18)).pack(pady=10)

        # Time Range Buttons
        time_ranges = [("Last Day", 1), ("Last 7 Days", 7), ("Last 30 Days", 30), ("Last 1 Year", 365)]
        for label, days in time_ranges:
            tk.Button(self.root, text=label, width=20, bg="lightblue", command=lambda d=days: self.generate_report(d), font=("Arial", 13, "bold")).pack(pady=5)

        # Custom Date Range Button
        tk.Button(self.root, text="Custom Date Range", bg="lightgreen", width=20, command=self.custom_date_range_picker, font=("Arial", 13, "bold")).pack(pady=10)

        # Report Display Area
        self.report_text = tk.Text(self.root, height=24, width=100, state='disabled')
        self.report_text.pack(pady=10)

        # Close Button
        tk.Button(self.root, text="Close", width=20, command=self.close_report, font=("Arial", 13), bg="red", fg="white").pack(pady=10)

    def generate_report(self, days):
        """Fetch and display sales data for the given time range."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        self.fetch_and_display_data(start_date, end_date)

    def custom_date_range_picker(self):
        """Open a custom date range picker using tkcalendar."""
        picker_window = tk.Toplevel(self.root)
        picker_window.title("Select Date Range")
        picker_window.geometry("500x300")
        center_window(picker_window, 600, 300)

        # Start Date Calendar
        tk.Label(picker_window, text="Start Date:", font=("Arial", 13, "bold")).grid(row=0, column=0, padx=20, pady=5, sticky="w")
        start_calendar = Calendar(picker_window)
        start_calendar.grid(row=1, column=0, padx=20, pady=5)

        # End Date Calendar
        tk.Label(picker_window, text="End Date:", font=("Arial", 13, "bold")).grid(row=0, column=1, padx=20, pady=5, sticky="w")
        end_calendar = Calendar(picker_window)
        end_calendar.grid(row=1, column=1, padx=20, pady=5)

        # Submit Button (centered below the calendars)
        tk.Button(picker_window, text="Generate Report", command=lambda: submit_dates(), font=("Arial", 14, "bold"), bg="lightgreen").grid(row=2, column=0, columnspan=2, pady=20)

        def submit_dates():
            start_date = datetime.strptime(start_calendar.get_date(), "%m/%d/%y")
            end_date = datetime.strptime(end_calendar.get_date(), "%m/%d/%y")
            self.fetch_and_display_data(start_date, end_date)
            picker_window.destroy()  # Close the date picker window

    def fetch_and_display_data(self, start_date, end_date):
        """Fetch data from the database and display the aggregated report."""
        sales_data = self.db.get_sales_between_dates(start_date, end_date)

        # Handle empty results
        if not sales_data:
            messagebox.showinfo("No Data", "No sales data found for the selected range.")
            return

        # Aggregate sales data by item name
        aggregated_data = {}
        for item in sales_data:
            name = item[3]          # item_name at index 3
            quantity = item[5]      # quantity at index 5
            total_price = item[6]   # total_price at index 6

            if name in aggregated_data:
                aggregated_data[name]['quantity'] += quantity
                aggregated_data[name]['total_price'] += total_price
            else:
                aggregated_data[name] = {'quantity': quantity, 'total_price': total_price}

        # Sort aggregated data by quantity in descending order
        sorted_items = sorted(aggregated_data.items(), key=lambda x: x[1]['quantity'], reverse=True)

        # Find the most sold item (first item in the sorted list)
        most_sold_item = sorted_items[0]

        # Clear previous content
        self.report_text.config(state='normal')
        self.report_text.delete(1.0, tk.END)

        # Configure text tags for styling
        self.report_text.tag_configure("header", font=("Arial", 14, "bold"), foreground="blue")
        self.report_text.tag_configure("item", font=("Arial", 12), foreground="green")
        self.report_text.tag_configure("total", font=("Arial", 12, "bold"), foreground="purple")
        self.report_text.tag_configure("most_sold", font=("Arial", 12, "bold"), foreground="red")

        # Insert header
        self.report_text.insert(tk.END, f"Sales Report ({start_date.date()} to {end_date.date()}):\n\n", "header")
        
        total_sales = 0  # Track total revenue

        # Insert each item (now sorted by quantity)
        for name, data in sorted_items:
            quantity = data['quantity']
            total_price = data['total_price']
            total_sales += total_price  # Calculate total revenue
            
            self.report_text.insert(tk.END, f"Item: {name}  ||  Sold: {quantity}  ||  Total Sales: ${total_price:.2f}\n", "item")

        # Insert total revenue
        self.report_text.insert(tk.END, f"\nTotal Revenue: ${total_sales:.2f}\n", "total")
        
        # Insert most sold item
        self.report_text.insert(tk.END, f"\nMost Sold Item: {most_sold_item[0]} (Sold: {most_sold_item[1]['quantity']} units)", "most_sold")

        self.report_text.config(state='disabled')


    def close_report(self):
        self.root.destroy()
        # self.main_window.deiconify()
