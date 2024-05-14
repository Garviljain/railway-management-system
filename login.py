import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector
import os
import datetime
import hashlib
from interface import available_trains, open_book_train_window, open_cancel_booking_window, open_show_bookings_window, check_fare

# Function to encrypt passwords
def encrypt_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to authenticate user
def authenticate_user():
    def login_user():
        mobile = entry_mobile.get()
        password = entry_password.get()

        # Check if mobile number or password is empty
        if not mobile or not password:
            messagebox.showerror("Error", "Mobile number and password are required.")
            return

        # Encrypt the password
        hashed_password = encrypt_password(password)

        # Establish connection to MySQL database
        mn = mysql.connector.connect(host="localhost", user="Garvil", password="mysql@123", database="railway")
        cur = mn.cursor()

        # Query the database to check if the user exists
        cur.execute("SELECT * FROM users WHERE mobile = %s", (mobile,))
        user = cur.fetchone()

        if user:
            # Verify the password
            if user[2] == hashed_password:
                messagebox.showinfo("Success", "Login successful!")
                open_main_window()  # Call the function to open the main window
            else:
                messagebox.showerror("Error", "Incorrect password.")
        else:
            messagebox.showerror("Error", "User not found.")

        # Close database connection
        cur.close()
        mn.close()

    def register_user():
        mobile = entry_mobile.get()
        password = entry_password.get()

        # Check if mobile number or password is empty
        if not mobile or not password:
            messagebox.showerror("Error", "Mobile number and password are required.")
            return

        # Encrypt the password
        hashed_password = encrypt_password(password)

        # Establish connection to MySQL database
        mn = mysql.connector.connect(host="localhost", user="Garvil", password="mysql@123", database="railway")
        cur = mn.cursor()

        # Check if the mobile number already exists in the database
        cur.execute("SELECT * FROM users WHERE mobile = %s", (mobile,))
        user_exists = cur.fetchone()

        if user_exists:
            messagebox.showerror("Error", "User already exists.")
        else:
            # Insert the new user into the database
            cur.execute("INSERT INTO users (mobile, hashed_password) VALUES (%s, %s)", (mobile, hashed_password))
            mn.commit()
            messagebox.showinfo("Success", "User registered successfully.")

        # Close database connection
        cur.close()
        mn.close()

    # Create the login/signup window
    login_window = tk.Tk()
    login_window.title("User Login/Registration")
    
    login_window = tk.Tk()
    login_window.title("User Login")
    login_window.geometry("300x200")

    # Styling
    login_window.configure(bg="#f0f0f0")
    label_font = ("Arial", 12)
    entry_font = ("Arial", 12)
    
    label_mobile = tk.Label(login_window, text="Mobile Number:")
    label_mobile.grid(row=0, column=0, padx=5, pady=5)

    entry_mobile = tk.Entry(login_window)
    entry_mobile.grid(row=0, column=1, padx=5, pady=5)

    label_password = tk.Label(login_window, text="Password:")
    label_password.grid(row=1, column=0, padx=5, pady=5)

    entry_password = tk.Entry(login_window, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    button_login = tk.Button(login_window, text="Login", command=login_user)
    button_login.grid(row=2, column=0, padx=5, pady=5)

    button_register = tk.Button(login_window, text="Register", command=register_user)
    button_register.grid(row=2, column=1, padx=5, pady=5)

# Function for the main application window
def open_main_window():
    # Create main window
    root = tk.Toplevel()
    root.title("Train Booking System")

    # Create labels and entry fields
    label_start_station = tk.Label(root, text="From Station Name:")
    label_start_station.grid(row=0, column=0, padx=5, pady=5)
    entry_start_station = tk.Entry(root)
    entry_start_station.grid(row=0, column=1, padx=5, pady=5)

    label_final_station = tk.Label(root, text="To Station Name:")
    label_final_station.grid(row=1, column=0, padx=5, pady=5)
    entry_final_station = tk.Entry(root)
    entry_final_station.grid(row=1, column=1, padx=5, pady=5)

    label_date = tk.Label(root, text="Date (YYYY-MM-DD):")
    label_date.grid(row=2, column=0, padx=5, pady=5)
    entry_date = tk.Entry(root)
    entry_date.grid(row=2, column=1, padx=5, pady=5)

    # Button to search for available trains
    button_search = tk.Button(root, text="Search", command=available_trains)
    button_search.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    # Treeview to display results
    treeview = ttk.Treeview(root, columns=("Train No", "Source Station", "Destination Station", "Arrival Time", "Departure Time"))
    treeview.heading("#0", text="Index")
    treeview.heading("Train No", text="Train No")
    treeview.heading("Source Station", text="Source Station")
    treeview.heading("Destination Station", text="Destination Station")
    treeview.heading("Arrival Time", text="Arrival Time")
    treeview.heading("Departure Time", text="Departure Time")
    treeview.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Label to display search result or error message
    result_text = tk.StringVar()
    label_result = tk.Label(root, textvariable=result_text)
    label_result.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # Button to open book train windowa
    button_book_train = tk.Button(root, text="Book Train", command=open_book_train_window)
    button_book_train.grid(row=6, column=0, padx=5, pady=5)

    # Button to open show bookings window
    button_show_bookings = tk.Button(root, text="Show Bookings", command= open_show_bookings_window)
    button_show_bookings.grid(row=7, column=0, padx=5, pady=5)

    # Button to open cancel booking window
    button_cancel_booking = tk.Button(root, text="Cancel Booking", command=open_cancel_booking_window)
    button_cancel_booking.grid(row=8, column=0, padx=5, pady=5)

    # Button to check fare
    button_check_fare = tk.Button(root, text="Check Fare", command=check_fare)
    button_check_fare.grid(row=9, column=0, padx=5, pady=5)

    # Text widget to display fare
    fare_text = tk.Text(root, height=10, width=50)
    fare_text.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

# Create the root window
root = tk.Tk()
root.title("User Authentication")

# Check user authentication before opening the main application window
authenticate_user()

root.mainloop()
