import uuid
from datetime import datetime
from fuzzywuzzy import process
from prettytable import PrettyTable

from contact import Contact
from custom_logger import logger

OPERATIONS = {
    'C': 'Create',
    'Q': 'Fuzzy Query',
    'F': 'Load contacts from a CSV file',
    'U': 'Update',
    'D': 'Delete',
    'E': 'Exit',
    'L': 'List'
}


class PhoneBook:
    def __init__(self):
        self.contacts = {}  # uuid.UUID => Contact
        self.logs = {}
        self.options = OPERATIONS

    def add_contact(self, contact_dict):
        contact = Contact(contact_dict)
        self.contacts[contact.guid] = contact
        logger.warning(contact.guid)

    def delete_contact(self, contact: Contact):
        contact.delete()
        logger.warning(contact.guid)

    def count_contacts(self):
        counter = 0
        for _, contact in self.contacts.items():
            if not contact.is_deleted():
                counter += 1
        return counter

    def search_contact(self, query):
        contact_details = []
        contact_list = []
        for _, contact in self.contacts.items():
            if contact.is_deleted():
                continue

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
            logger.warning(contact_list[matched_index].guid)
            return contact_list[matched_index]
        return 'No contact found!'

    def get_contact_by_id(self, guid):
        for _, contact in self.contacts.items():
            if uuid.UUID(guid) == contact.guid:
                return contact

        return None

    def update_contact(self, contact: Contact):
        self.contacts[contact.guid] = Contact({
            "guid": contact.guid,
            "first_name": contact.first_name,
            "last_name": contact.last_name,
            "phone": contact.phone,
            "email": contact.email,
            "address": contact.address,
        }, is_new=False)
        logger.warning(contact.guid)
        print(self.contacts[contact.guid])

    def list_contacts(self):
        if self.count_contacts():
            phone_table = PrettyTable()
            phone_table.field_names = ["ID", "First Name", "Last Name", "Phone",
                                       "Email", "Address"]
            for guid, contact in self.contacts.items():
                if contact.is_deleted():
                    continue
                phone_table.add_row(
                    [guid, contact.first_name, contact.last_name,
                     contact.phone, contact.email,
                     contact.address])
            print(phone_table)
        else:
            print("No contacts found.")
