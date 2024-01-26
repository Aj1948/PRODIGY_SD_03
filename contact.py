import sqlite3
import tkinter as tk
from tkinter import ttk

class ContactManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Management System")
        self.create_database()
        self.create_gui()

    def create_database(self):
        self.conn = sqlite3.connect("contacts.db")
        self.c = self.conn.cursor()
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                email TEXT
            )
        ''')
        self.conn.commit()

    def create_gui(self):
        self.tree = ttk.Treeview(self.root, columns=("ID", "Name", "Phone", "Email"), show="headings")

        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")

        self.tree.pack(padx=10, pady=10)

        add_button = tk.Button(self.root, text="Add Contact", command=self.add_contact)
        add_button.pack(pady=5)

        delete_button = tk.Button(self.root, text="Delete Contact", command=self.delete_contact)
        delete_button.pack(pady=5)

        edit_button = tk.Button(self.root, text="Edit Contact", command=self.edit_contact)
        edit_button.pack(pady=5)

        self.load_contacts()

    def load_contacts(self):
        self.tree.delete(*self.tree.get_children())
        self.c.execute("SELECT * FROM contacts")
        contacts = self.c.fetchall()
        for contact in contacts:
            self.tree.insert("", "end", values=contact)

    def add_contact(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Add Contact")

        tk.Label(add_window, text="Name:").pack(pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.pack(pady=5)

        tk.Label(add_window, text="Phone:").pack(pady=5)
        phone_entry = tk.Entry(add_window)
        phone_entry.pack(pady=5)

        tk.Label(add_window, text="Email:").pack(pady=5)
        email_entry = tk.Entry(add_window)
        email_entry.pack(pady=5)

        add_button = tk.Button(add_window, text="Add", command=lambda: self.save_contact(
            name_entry.get(), phone_entry.get(), email_entry.get(), add_window))
        add_button.pack(pady=5)

    def save_contact(self, name, phone, email, window):
        self.c.execute("INSERT INTO contacts (name, phone, email) VALUES (?, ?, ?)", (name, phone, email))
        self.conn.commit()
        self.load_contacts()
        window.destroy()

    def delete_contact(self):
        selected_item = self.tree.selection()
        if selected_item:
            contact_id = self.tree.item(selected_item, "values")[0]
            self.c.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
            self.conn.commit()
            self.load_contacts()
        else:
            tk.messagebox.showwarning("Error", "Please select a contact to delete.")

    def edit_contact(self):
        selected_item = self.tree.selection()
        if selected_item:
            contact_id, name, phone, email = self.tree.item(selected_item, "values")

            edit_window = tk.Toplevel(self.root)
            edit_window.title("Edit Contact")

            tk.Label(edit_window, text="Name:").pack(pady=5)
            name_entry = tk.Entry(edit_window)
            name_entry.insert(0, name)
            name_entry.pack(pady=5)

            tk.Label(edit_window, text="Phone:").pack(pady=5)
            phone_entry = tk.Entry(edit_window)
            phone_entry.insert(0, phone)
            phone_entry.pack(pady=5)

            tk.Label(edit_window, text="Email:").pack(pady=5)
            email_entry = tk.Entry(edit_window)
            email_entry.insert(0, email)
            email_entry.pack(pady=5)

            save_button = tk.Button(edit_window, text="Save", command=lambda: self.update_contact(
                contact_id, name_entry.get(), phone_entry.get(), email_entry.get(), edit_window))
            save_button.pack(pady=5)
        else:
            tk.messagebox.showwarning("Error", "Please select a contact to edit.")

    def update_contact(self, contact_id, name, phone, email, window):
        self.c.execute("UPDATE contacts SET name=?, phone=?, email=? WHERE id=?", (name, phone, email, contact_id))
        self.conn.commit()
        self.load_contacts()
        window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactManagementSystem(root)
    root.mainloop()
