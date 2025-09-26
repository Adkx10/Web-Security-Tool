import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

# Main
def combined_functions(event=None):
    # Enable editing in output box
    txt_output.config(state="normal")
    txt_output.delete("1.0", tk.END)

    # NAME & EMAIL VALIDATION
    name = ent_name.get().strip()
    email = ent_email.get().strip()
    age = ent_age.get().strip()
    message = txt_msg.get("1.0", tk.END).strip()
        
    #NAME, EMAIL, AND AGE VALIDATOR (via Flask API)    
    try:
        response = requests.post(
            "http://127.0.0.1:5000/validate",
            json={"name": name, "email": email, "age": age, "message": message}
        )
        if response.status_code != 200:
            messagebox.showerror("Error", f"API error: {response.text}")
            return
        
        results = response.json()

        # validate email
        if not results["email"]["is_valid"]:
            messagebox.showerror("Validation Result", results["email"]["result"])
            return
        print_valid_email = email
        
        # validate name
        if not results["name"]["is_valid"]:
            messagebox.showerror("Validation Result", results["name"]["result"])
            return
        print_valid_name = name
        
        # validate age
        print_valid_age = results["age"]["result"]
            
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Could not connect to the server: {e}")
        return

    txt_output.insert(tk.END, f"Full Name: {print_valid_name}\n")
    txt_output.insert(tk.END, f"Email Address: {print_valid_email}\n")
    txt_output.insert(tk.END, f"Age: {print_valid_age}\n")

    # MESSAGE
    print_valid_msg = results["message"]["result"]

    if results["message"]["is_valid"] and print_valid_msg.startswith("Valid URL:"):
        clean_url = print_valid_msg.replace("Valid URL:", "").strip()
        try:
            response = requests.get(clean_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            txt_output.insert(tk.END, f"\n\nMessage/URL: {clean_url}")
            txt_output.insert(tk.END, "\nHeadings:\n")
            headings = soup.find_all(['h1','h2','h3','h4','h5','h6'])
            for heading in headings:
                txt_output.insert(tk.END, f"{heading.name}: {heading.text.strip()}\n")
            
            txt_output.insert(tk.END, "\nHyperlinks:\n")
            links = soup.find_all('a', href=True)
            for link in links:
                text = link.text.strip()
                href = link['href']
                txt_output.insert(tk.END, f"Text: {text} | URL: {href}\n")

        except requests.exceptions.RequestException as e:
            txt_output.insert(tk.END, f"\n\nAn error occurred while fetching the webpage: {e}")
    else:
        txt_output.insert(tk.END, f"\n\nMessage: {print_valid_msg}")

    # Lock output box
    txt_output.config(state="disabled")

window = tk.Tk()
window.title('Web Form Input Validator and Sanitizer')
window.configure(background='black')

frm_main = tk.Frame(window, bg='black', relief="sunken", borderwidth=10)

# Labels
lbl_window = tk.Label(frm_main, text='User Input Validation and Sanitizer', relief='raised', bg='orange', font=('Arial', 15))
lbl_name = tk.Label(frm_main, bg='black', fg='lightgreen', text='Full Name: ')
lbl_email = tk.Label(frm_main, bg='black', fg='lightgreen', text='Email Address: ')
lbl_age = tk.Label(frm_main, bg='black', fg='lightgreen', text='Age (Optional): ')
lbl_msg = tk.Label(frm_main, bg='black', fg='lightgreen', text='Message (Optional): ')
lbl_output = tk.Label(frm_main, bg='black', fg='lightgreen', text='Output: ')

# Entries & Text Fields
ent_name = tk.Entry(frm_main, bg='gray', fg='yellow',  bd=2)
ent_email = tk.Entry(frm_main, bg='gray', fg='yellow', bd=2)
ent_age = tk.Entry(frm_main, bg='gray', fg='yellow', bd=2)
txt_msg = tk.Text(frm_main, bg='gray', fg='yellow', height=5, width=50, bd=2)
#txt_output = tk.Text(frm_main, bg='gray', fg='yellow', height=10, width=50, state='disabled', bd=2)
txt_output = scrolledtext.ScrolledText(frm_main, bg='gray', fg='yellow', height=15, width=98, state='disabled', bd=2)

# Buttons
btn_submit = tk.Button(frm_main, text='Submit', bg='orange', bd=2, command=combined_functions)

# Grid
frm_main.grid(row=0, column=0, padx=100, pady=20)
lbl_window.grid(row=0, column=0, columnspan=2, ipady=3, pady=5, sticky='nsew')
lbl_name.grid(row=1, column=0, sticky='e')
lbl_email.grid(row=2, column=0, sticky='e')
lbl_age.grid(row=3, column=0, sticky='e')
lbl_msg.grid(row=4, column=0, sticky='ne')
lbl_output.grid(row=6, column=0, sticky='ne')

ent_name.grid(row=1, column=1, pady=3, sticky='ew')
ent_email.grid(row=2, column=1, pady=3, sticky='ew')
ent_age.grid(row=3, column=1, pady=3, sticky='w')
txt_msg.grid(row=4, column=1, pady=3, sticky='ew')
#txt_output.grid(row=5, column=1, pady=3)
txt_output.grid(row=6, column=1, pady=3)

btn_submit.grid(row=5, column=0, columnspan=2, ipady=3, ipadx=3, pady=5)


window.mainloop()

