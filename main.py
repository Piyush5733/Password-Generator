from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)  # join all the items in the list

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    my_password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "my_password": my_password
        }
    }

    if len(website) == 0 or len(email) == 0 or len(my_password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any field empty.")
    else:
        # is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\nEmail: {email}."
        #                                                         f"\nPassword: {my_password}.\nIs it ok to save?")
        # if is_ok:   #indented
        try:
            with open("data.json", "r") as data_file:
                # reading old data
                data = json.load(data_file)

        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                # saving updated data
                json.dump(new_data, data_file, indent=4)

        else:
            # updating old data with new data
            data.update(new_data)
            with open("data.json", "w") as data_file:
                # saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    website = website_entry.get()
    try:
        with open("data.json") as data_file:
            # access or read the data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="ERROR", message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["my_password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="ERROR", message=f"No detail of {website} exist")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("PASSWORD MANAGER")
window.config(padx=50, pady=50)   # gap b/w wall and image in x and y direction

canvas = Canvas(width=200, height=200)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

# labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# entries
website_entry = Entry(width=35)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = Entry(width=55)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "ENTER EMAIL ID")
password_entry = Entry(width=35)
password_entry.grid(column=1, row=3)

# buttons
gen_pass_button = Button(text="Generate Password", command=password_generator)
gen_pass_button.grid(column=2, row=3)
Add_button = Button(text="Add", width=46, command=save)
Add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1, sticky="w")  # align to left within it's column

window.mainloop()

