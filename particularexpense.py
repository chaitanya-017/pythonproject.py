from tkinter import *
from tkinter import ttk
import sqlite3 as db
from tkcalendar import DateEntry
from datetime import datetime

def init():
    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()
    query = '''
    CREATE TABLE IF NOT EXISTS expenses (
        date TEXT,
        name TEXT,
        title TEXT,
        expense REAL
    )
    '''
    curr.execute(query)
    connectionObjn.commit()

def submitexpense():
    values = [dateEntry.get(), Name.get(), Title.get(), Expense.get()]

    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()
    query = '''
    INSERT INTO expenses VALUES 
    (?, ?, ?, ?)
    '''
    curr.execute(query, values)
    connectionObjn.commit()

    Etable.insert('', 'end', values=values)
    calculate_total_expenses()

def viewexpense():
    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()
    query = '''
    SELECT * FROM expenses
    '''
    curr.execute(query)
    rows = curr.fetchall()

    for i in Etable.get_children():
        Etable.delete(i)

    for row in rows:
        Etable.insert('', 'end', values=row)

    calculate_total_expenses()

def delete_selected():
    item = Etable.selection()[0]
    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()

    values = Etable.item(item, 'values')
    query = '''
    DELETE FROM expenses WHERE date=? AND name=? AND title=? AND expense=?
    '''
    curr.execute(query, values)
    connectionObjn.commit()
    viewexpense()

def calculate_total_expenses():
    total_expenses = 0
    for item in Etable.get_children():
        total_expenses += float(Etable.item(item, 'values')[3])

    total_label.config(text=f'Total Expenses: Rs{total_expenses:.2f}')

def calculate_expenses_for_month():
    selected_month = selected_month_var.get()
    total_expenses_month = 0
    for item in Etable.get_children():
        if get_month_from_date(Etable.item(item, 'values')[0]) == selected_month:
            total_expenses_month += float(Etable.item(item, 'values')[3])

    total_label_month.config(text=f'Total Expenses for {selected_month}: Rs{total_expenses_month:.2f}')

def get_selected_month():
    today = datetime.today()
    return today.strftime("%B")

def get_month_from_date(date_string):
    date_object = datetime.strptime(date_string, "%m/%d/%y")
    return date_object.strftime("%B")

def calculate_expenses_for_item(item_title):
    total_expenses_item = 0
    for item in Etable.get_children():
        if Etable.item(item, 'values')[2] == item_title:
            total_expenses_item += float(Etable.item(item, 'values')[3])

    total_label_item.config(text=f'Total Expenses for {item_title}: Rs{total_expenses_item:.2f}')

root = Tk()
root.title("Chaitanya Expense tracker")
root.geometry('1000x900')

dateLabel = Label(root, text="Date", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
dateLabel.grid(row=0, column=0, padx=7, pady=7)

dateEntry = DateEntry(root, width=12, font=('arial', 15, 'bold'))
dateEntry.grid(row=0, column=1, padx=7, pady=7)

Name = StringVar()
nameLabel = Label(root, text="Name", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
nameLabel.grid(row=1, column=0, padx=7, pady=7)

NameEntry = Entry(root, textvariable=Name, font=('arial', 15, 'bold'))
NameEntry.grid(row=1, column=1, padx=7, pady=7)

Title = StringVar()
titleLabel = Label(root, text="Title", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
titleLabel.grid(row=2, column=0, padx=7, pady=7)

titleEntry = Entry(root, textvariable=Title, font=('arial', 15, 'bold'))
titleEntry.grid(row=2, column=1, padx=7, pady=7)

Expense = IntVar()
expenseLabel = Label(root, text="Expense", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
expenseLabel.grid(row=3, column=0, padx=7, pady=7)

expenseEntry = Entry(root, textvariable=Expense, font=('arial', 15, 'bold'))
expenseEntry.grid(row=3, column=1, padx=7, pady=7)

submitbtn = Button(root, command=submitexpense, text="Submit", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
submitbtn.grid(row=4, column=0, padx=13, pady=13)

viewtn = Button(root, command=viewexpense, text="View expenses", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=12)
viewtn.grid(row=4, column=1, padx=13, pady=13)

deletebtn = Button(root, text="Delete selected", command=delete_selected, font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white", width=15)
deletebtn.grid(row=4, column=2, padx=13, pady=13)

Elist = ['Date', 'Name', 'Title', 'Expense']
Etable = ttk.Treeview(root, column=Elist, show='headings', height=7)
for c in Elist:
    Etable.heading(c, text=c.title())
Etable.grid(row=5, column=0, padx=7, pady=7, columnspan=4)

total_label = Label(root, text="Total Expenses: Rs0.00", font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white")
total_label.grid(row=6, column=0, columnspan=4, pady=10)

selected_month_var = StringVar()
selected_month_var.set(get_selected_month())

selected_month_label = Label(root, text="Selected Month: ", font=('arial', 15, 'bold'))
selected_month_label.grid(row=7, column=0, padx=7, pady=7)

selected_month_dropdown = ttk.Combobox(root, textvariable=selected_month_var, values=[
    "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
selected_month_dropdown.grid(row=7, column=1, padx=7, pady=7)

calculate_month_btn = Button(root, text="Calculate Total for Selected Month", command=calculate_expenses_for_month,
                             font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white")
calculate_month_btn.grid(row=7, column=2, padx=7, pady=7)

total_label_month = Label(root, text="Total Expenses for Month: Rs0.00", font=('arial', 15, 'bold'),
                          bg="DodgerBlue2", fg="white")
total_label_month.grid(row=8, column=0, columnspan=4, pady=10)

item_title_var = StringVar()
item_title_var.set("")  # Set the default value to an empty string

item_title_label = Label(root, text="Enter Item Title: ", font=('arial', 15, 'bold'))
item_title_label.grid(row=9, column=0, padx=7, pady=7)

item_title_entry = Entry(root, textvariable=item_title_var, font=('arial', 15, 'bold'))
item_title_entry.grid(row=9, column=1, padx=7, pady=7)

calculate_item_btn = Button(root, text="Calculate Total for Item", command=lambda: calculate_expenses_for_item(item_title_var.get()),
                             font=('arial', 15, 'bold'), bg="DodgerBlue2", fg="white")
calculate_item_btn.grid(row=9, column=2, padx=7, pady=7)

total_label_item = Label(root, text="Total Expenses for Item: Rs0.00", font=('arial', 15, 'bold'),
                          bg="DodgerBlue2", fg="white")
total_label_item.grid(row=10, column=0, columnspan=4, pady=10)

init()

root.mainloop()
