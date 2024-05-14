import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import core.User_Functions as user
import datetime

sleeper_charge = int(1.5)
third_ac_charge = int(2)
second_ac_charge = int(3)
first_ac_charge = int(4)


def available_trains():
    # Function to search for available trains based on user input
    start_station = entry_start_station.get()
    final_station = entry_final_station.get()
    date_str = entry_date.get()
    
    try:
        # Convert date string to datetime object
        date_user = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        current_date = datetime.date.today()
        max_date = current_date + datetime.timedelta(days=30)  # Assuming maximum booking allowed for 30 days
        if date_user < current_date or date_user > max_date:
            raise ValueError("Please enter a valid date within the next 30 days.")
    except ValueError as e:
        result_text.set(str(e))
        return

    # Establish connection to MySQL database
    mn = mysql.connector.connect(host="localhost", user="Garvil", password="mysql@123", database="railway")
    cur = mn.cursor()

    # Query database for available trains
    query = 'SELECT Train_No, Source_Station_Name, Destination_Station_Name, Arrival_Time, Departure_Time FROM train_info WHERE Source_Station_Name=%s AND Destination_Station_Name=%s;'
    cur.execute(query, (start_station, final_station))
    result = cur.fetchall()

    # Display results in the treeview
    for row in treeview.get_children():
        treeview.delete(row)
    if result:
        for train in result:
            treeview.insert("", "end", values=train)
        result_text.set("Total of {} records found.".format(len(result)))
    else:
        result_text.set("No trains available.")

    # Close database connection
    cur.close()
    mn.close()


def open_book_train_window():
    book_train_window = tk.Toplevel(root)
    book_train_window.title("Book Train")

    # Widgets
    label_train_no = tk.Label(book_train_window, text="Train Number:")
    label_train_no.pack()

    entry_train_no = tk.Entry(book_train_window)
    entry_train_no.pack()

    label_name = tk.Label(book_train_window, text="Passenger Name:")
    label_name.pack()

    entry_name = tk.Entry(book_train_window)
    entry_name.pack()

    label_mobile = tk.Label(book_train_window, text="Mobile Number:")
    label_mobile.pack()

    entry_mobile = tk.Entry(book_train_window)
    entry_mobile.pack()

    label_adhaar = tk.Label(book_train_window, text="Adhaar Number:")
    label_adhaar.pack()

    entry_adhaar = tk.Entry(book_train_window)
    entry_adhaar.pack()

    label_class = tk.Label(book_train_window, text="Class:")
    label_class.pack()

    class_var = tk.StringVar(book_train_window)
    class_var.set("Sleeper")  # Default value

    option_menu = tk.OptionMenu(book_train_window, class_var, "Sleeper", "AC-1", "AC-2", "AC-3")
    option_menu.pack()

    # Functionality
    def book_train():
        # Collect user input data
        booking_data = {
            "train_no": entry_train_no.get(),
            "Name": entry_name.get(),
            "Mobile": entry_mobile.get(),
            "adhaar": entry_adhaar.get(),
            "Class": class_var.get()
        }
        booking_data["Time_of_Booking"] = datetime.datetime.now().strftime("%d-%m-%y")

        # Validate mobile number
        if not booking_data["Mobile"].isdigit() or len(booking_data["Mobile"]) != 10:
            messagebox.showerror("Invalid Input", "Please enter a valid 10-digit mobile number.")
            return

        # Validate adhaar number
        if not booking_data["adhaar"].isdigit() or len(booking_data["adhaar"]) != 12:
            messagebox.showerror("Invalid Input", "Please enter a valid 12-digit adhaar number.")
            return

        # Call the BookTrain function and pass the dictionary containing booking data
        user.BookTrain(booking_data)

        # Perform any necessary actions after booking
        messagebox.showinfo("Booking", "Booking successful!")

    button_book = tk.Button(book_train_window, text="Book Train", command=book_train)
    button_book.pack()


def open_show_bookings_window():
    def show_bookings():
        mobile_no = entry_mobile.get()

        # Call the ShowBookings function and pass the mobile number
        bookings = user.ShowBookings(mobile_no)

        if bookings is None:
            messagebox.showinfo("No Records Found", "No bookings found for the provided mobile number.")
        else:
            if len(bookings) == 0:
                messagebox.showinfo("No Records Found", "No bookings found for the provided mobile number.")
            else:
                # Clear any existing rows in the treeview
                for row in tree.get_children():
                    tree.delete(row)

                # Populate the treeview with the bookings data
                for booking in bookings:
                    tree.insert('', 'end', values=booking)

    show_bookings_window = tk.Toplevel(root)
    show_bookings_window.title("Show Bookings")

    label_mobile = tk.Label(show_bookings_window, text="Enter Your 10 Digit Mobile Number:")
    label_mobile.pack()

    entry_mobile = tk.Entry(show_bookings_window)
    entry_mobile.pack()

    button_show = tk.Button(show_bookings_window, text="Show Bookings", command=show_bookings)
    button_show.pack()

    # Create a Treeview widget to display bookings in tabular format
    tree = ttk.Treeview(show_bookings_window, columns=("Train No", "Passenger Name", "Mobile No", "Passenger Aadhaar", "Time of Booking", "Booking ID", "Class"), show="headings")
    tree.heading("Train No", text="Train No")
    tree.heading("Passenger Name", text="Passenger Name")
    tree.heading("Mobile No", text="Mobile No")
    tree.heading("Passenger Aadhaar", text="Passenger Aadhaar")
    tree.heading("Time of Booking", text="Time of Booking")
    tree.heading("Booking ID", text="Booking ID")
    tree.heading("Class", text="Class")
    tree.pack()


def open_cancel_booking_window():
    def cancel_booking():
        try:
            unique_id = int(entry_unique_id.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid ID.")
            return

        if unique_id < 1 or unique_id > 10000:
            messagebox.showerror("Invalid Input", "ID out of range.")
            return

        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to cancel this booking?")
        if confirmation:
            user.CancelBooking(unique_id)
            messagebox.showinfo("Cancellation", "Booking cancelled successfully!")

    cancel_booking_window = tk.Toplevel(root)
    cancel_booking_window.title("Cancel Booking")

    label_unique_id = tk.Label(cancel_booking_window, text="Enter Unique ID:")
    label_unique_id.pack()

    entry_unique_id = tk.Entry(cancel_booking_window)
    entry_unique_id.pack()

    button_cancel = tk.Button(cancel_booking_window, text="Cancel Booking", command=cancel_booking)
    button_cancel.pack()


# Define the function to calculate fare based on distance
def check_fare():
    start_station = entry_start_station.get()
    final_station = entry_final_station.get()

    try:
        # Establish connection to MySQL database
        mn = mysql.connector.connect(host="localhost", user="Garvil", password="mysql@123", database="railway")
        cur = mn.cursor()

        # Query database for train information
        query = 'SELECT Train_No, Distance FROM train_info WHERE Source_Station_Name=%s AND Destination_Station_Name=%s;'
        cur.execute(query, (start_station, final_station))
        result_fare = cur.fetchall()

        if not result_fare:
            result_text.set("No available trains!")
            return

        # Display result in the text widget
        fare_text.delete("1.0", "end")
        for row in result_fare:
            fare_text.insert("end", f"{row[0]} sleeper_charge: Rs. {int(row[1]) * sleeper_charge}\n third_ac_charge: Rs. {int(row[1]) * third_ac_charge}\n second_ac_charge Rs. {int(row[1]) * second_ac_charge}\n first ac charge :Rs. {int(row[1]) * first_ac_charge}\n")

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"An error occurred: {err}")
    finally:
        # Close database connection
        if 'mn' in locals():
            cur.close()
            mn.close()

# Main window
root = tk.Tk()
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

# Button to open book train window
button_book_train = tk.Button(root, text="Book Train", command=open_book_train_window)
button_book_train.grid(row=6, column=0, padx=5, pady=5)

# Button to open show bookings window
button_show_bookings = tk.Button(root, text="Show Bookings", command=open_show_bookings_window)
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

root.mainloop()
