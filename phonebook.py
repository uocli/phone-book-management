from datetime import datetime

from prettytable import PrettyTable

from contact import Contact


class PhoneBook:
    def __init__(self):
        self.contacts = {}
        self.logs = {}
        self.options = {
            'C': 'Create',
            'R': 'Retrieve',
            'U': 'Update',
            'D': 'Delete',
            'E': 'Exit',
            'L': 'List',
            'G': 'Get Option List',
            'A': 'Admin'
        }

    def add_contact(self, firs_name, last_name, phone, email, address):
        contact = Contact(firs_name, last_name, phone, email,
                          address)
        self.contacts[contact.guid] = contact

    def delete_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            print(f"Contact '{name}' deleted.")
        else:
            print(f"Contact '{name}' not found.")

    def search_contact(self, name):
        phone = self.contacts.get(name)
        if phone:
            print(f"Contact '{name}': {phone}")
        else:
            print(f"Contact '{name}' not found.")

    def list_contacts(self):
        if self.contacts:
            print("Contacts:")
            phone_table = PrettyTable()
            phone_table.field_names = ["ID", "First Name", "Last Name", "Phone",
                                       "Email", "Address"]
            for key, contact in self.contacts.items():
                phone_table.add_row(
                    [contact.guid, contact.first_name, contact.last_name,
                     contact.phone, contact.email,
                     contact.address])
            print(phone_table)
        else:
            print("No contacts found.")

    def add_log(self, guid, operation):
        if guid and guid not in self.logs:
            self.logs[guid] = []
        self.logs[guid].append(
            datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + operation)


def is_phone_number():
    pass
