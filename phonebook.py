from datetime import datetime
# from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from prettytable import PrettyTable

from contact import Contact

OPERATIONS = {
    'C': 'Create',
    'Q  ': 'Fuzzy Query',
    'F': 'Load contacts from a CSV file',
    'U': 'Update',
    'D': 'Delete',
    'E': 'Exit',
    'L': 'List',
    'G': 'Get Option List',
    'A': 'Admin'
}


class PhoneBook:
    def __init__(self):
        self.contacts = {}
        self.logs = {}
        self.options = OPERATIONS

    def add_contact(self, contact_dict):
        contact = Contact(contact_dict)
        self.contacts[contact.guid] = contact

    def delete_contact(self, name):
        if name in self.contacts:
            del self.contacts[name]
            print(f"Contact '{name}' deleted.")
        else:
            print(f"Contact '{name}' not found.")

    def search_contact(self, query):
        contact_details = []
        contact_list = []
        for _, contact in self.contacts.items():
            details = [
                f"{contact.first_name}",
                f"{contact.last_name}",
                f"{contact.phone}",
                f"{contact.email}",
                f"{contact.address}"
            ]
            contact_list.append(contact)
            contact_details.append(" | ".join(details))
        best_match = process.extractOne(query, contact_details)

        if best_match:
            matched_index = contact_details.index(best_match[0])
            return contact_list[matched_index]
        return 'No contact found!'

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
