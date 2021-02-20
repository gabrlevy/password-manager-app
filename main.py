from tkinter import *
from tkinter import messagebox
FONT_NAME = "Courier"
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
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
    password = ''.join(password_list)

    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SEARCH ENTRY ------------------------------- #
def search_entry():
    website = website_input.get()
    try:
        with open("my_passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="No Matches", message=f"No password for {website} was found")
    else:
        if website in data:
            username = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"{website} \nusername: {username} \npassword: {password}")
        else:
            messagebox.showinfo(title=website, message=f"{website} \nno username or password were found for this site")



# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    if len(website) < 1 or len(password) < 1:
        messagebox.showinfo(title="check info", message=f"you left blank fields")
    else:
        try:
            with open("my_passwords.json", "r") as file:
                # reading saved data
                data = json.load(file)
        except FileNotFoundError:
            with open("my_passwords.json", "w") as file:
                # saving updated data
                json.dump(new_data, file, indent=4)
        else:
            # updating old data with new one
            data.update(new_data)

            with open("my_passwords.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
                website_input.delete(0, END)
                password_input.delete(0, END)
                messagebox.showinfo(title="confirmed", message=f"Success, your password for {website} was saved")




# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:", font=(FONT_NAME, 12, "bold"))
website_label.grid(column=0, row=1)

website_input = Entry()
website_input.grid(column=1, row=1)
website_input.focus()

username_label = Label(text="Email/Username:", font=(FONT_NAME, 12, "bold"))
username_label.grid(column=0, row=2)

username_input = Entry(width=35)
username_input.grid(column=1, row=2, columnspan=2)
# ------------------------ insert your most common username or email------------------#
username_input.insert(0, "your@mail.com")

password_label = Label(text="Password:", font=(FONT_NAME, 12, "bold"))
password_label.grid(column=0, row=3)

password_input = Entry(width=21)
password_input.grid(column=1, row=3)

search_button = Button(text="           Search          ", highlightthickness=0, command=search_entry)
search_button.grid(column=2, row=1)

add_button = Button(text="Add", highlightthickness=0, width=36, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

generate_pw_button = Button(text="Generate Password", highlightthickness=0, command=generate_password)
generate_pw_button.grid(column=2, row=3)


window.mainloop()
