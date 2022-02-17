from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def password_generator():
    password_input.delete(0, END)
    password_letters = [choice(letters) for _ in range(randint(4, 6))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)
    password = "".join(password_list)
    password_input.insert(0, f"{password}")
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def data_check():
    website = website_input.get().lower()
    email = email_input.get().lower()
    password = password_input.get()
    if len(password) == 0 or len(email) == 0 or len(website) == 0:
        messagebox.showerror(title="Saving error", message="Website or email or password can't be empty!")
    else:
        is_ok = messagebox.askokcancel(title="Confirmation",
                                       message=f"Do you want to save this password?\nwebsite: {website}\nemail: {email}"
                                               f"\npassword: {password}")
        if is_ok:
            try:
                with open("data.json", "r") as file:
                    data = json.load(file)
                    print(data)
                    if website in data:
                        new_password = messagebox.askokcancel(title="Confirmation",
                                                              message=f"Password for this website already exist. Do "
                                                                      f"you want to "
                                                                      f"overwrite?")
                        if new_password:
                            save()
                        else:
                            messagebox.showinfo(title="Confirmation", message="Saving password has been canceled")
                            return
                    else:
                        save()
            except FileNotFoundError:
                save()
        else:
            messagebox.showwarning(message="Saving password has been canceled")


def save():
    website = website_input.get().lower()
    email = email_input.get().lower()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            data.update(new_data)
    except FileNotFoundError:
        with open("data.json", "w") as file:
            json.dump(new_data, file, indent=4)
    else:
        with open("data.json", "w") as file:
            json.dump(data, file, indent=4)

    website_input.delete(0, "end")
    password_input.delete(0, "end")
    messagebox.showinfo(title="Confirmation", message="Password saved successfully!")


# -------------------------FINDING PASSWORD --------------------------- #

def find_password():
    try:
        with open("data.json", "r") as file:
            data = json.load(file)
            website = website_input.get().lower()
            saved_password = data[website]
            messagebox.showinfo(title="Password found!",
                                message=f"email: {saved_password['email']}\npassword: {saved_password['password']}")
    except KeyError:
        messagebox.showerror(message="No details for website exists!")
    except FileNotFoundError:
        messagebox.showerror(message="Uuups, no file with saved passwords found")


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.config(padx=50, pady=50)
window.title("Password manager")

label_website = Label(text="Website", font=("Arial", 10, "bold"))
label_website.grid(column=1, row=2)

label_email = Label(text="Email/Username", font=("Arial", 10, "bold"))
label_email.grid(column=1, row=3)

label_password = Label(text="Password", font=("Arial", 10, "bold"))
label_password.grid(column=1, row=4)

website_input = Entry(width=33)
website_input.grid(row=2, column=2)
website_input.focus()

email_input = Entry(width=52)
email_input.grid(row=3, column=2, columnspan=2)
email_input.insert(0, "bartlomiej.zelazko@gmail.com")

password_input = Entry(width=33)
password_input.grid(row=4, column=2)

generate_button = Button(text="Generate Password", command=password_generator)
generate_button.grid(column=3, row=4)

add_button = Button(text="Add", width=44, command=data_check)
add_button.grid(row=5, column=2, columnspan=2)

search_button = Button(text="Search", width=13, command=find_password)
search_button.grid(row=2, column=3)

canvas = Canvas(width=200, height=200, highlightthickness=0)
password_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=password_img)

canvas.grid(column=2, row=1)

window.mainloop()
