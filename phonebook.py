import uuid
from datetime import datetime

from fuzzywuzzy import process
from prettytable import PrettyTable

from contact import Contact
from custom_logger import logger
from utils import is_valid_phone_number, is_valid_email, is_valid_uuid

OPERATIONS = {
    'C': 'Create',
    'Q': 'Fuzzy Query',
    'F': 'Load contacts from a CSV file',
    'U': 'Update',
    'D': 'Delete',
    'E': 'Exit',
    'L': 'List',
    'LA': 'List in ascending order',
    'LD': 'List in descending order',
}


def sorting_contact(contacts, desc=False):
    """
    Sort a given dict by the last_name of the contacts
    :param contacts: contact dict (UUID: contact.Contact)
    :param desc: a boolean flag indicating the sorting order, asc by default.
    :return: new sorted contact dict
    """
    sorted_dict = dict(sorted(contacts.items(),
                              key=lambda item: item[1].last_name,
                              reverse=desc))
    new_contact_dict = {}
    for c in sorted_dict.items():
        new_contact_dict[c[1].guid] = c[1]

    return new_contact_dict


def count_contacts(contacts):
    """
    Count contacts which are not deleted in the phone book
    :param contacts: a given contact dict
    :return: an integer greater or equal to 0
    """
    counter = 0
    for _, contact in contacts.items():
        if not contact.is_deleted():
            counter += 1
    return counter


def list_contacts(contacts, start_date_str: str = None,
                  end_date_str: str = None):
    """
    List contacts created within the given time frame
    :param contacts: a contact dict (UUID: contact.Contact)
    :param start_date_str: start date string in format yyyy-MM-dd
    :param end_date_str: end date string in format yyyy-MM-dd
    :return: None
    """
    start_date = None
    end_date = None
    if start_date_str is not None:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

    if end_date_str is not None:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    if count_contacts(contacts):
        phone_table = PrettyTable()
        phone_table.field_names = ["ID", "First Name", "Last Name", "Phone",
                                   "Email", "Address", "Created Date"]
        for guid, contact in contacts.items():
            if contact.is_deleted():
                continue
            if start_date is not None and contact.created_date() < start_date:
                continue
            if end_date is not None and contact.created_date() > end_date:
                continue
            phone_table.add_row(
                [guid, contact.first_name, contact.last_name,
                 contact.phone, contact.email,
                 contact.address, contact.created_date()])
        print(phone_table)
    else:
        print("No contacts found.")


def create_contact_dict():
    """
    Create a contact manually
    :return: a contact dict
    """
    first_name = ''
    while not first_name:
        first_name = input("First Name (Required): ")

    last_name = ''
    while not last_name:
        last_name = input("Last Name (Required): ")

    phone = ''
    while not is_valid_phone_number(phone):
        phone = input("Phone in format (xxx) xxx-xxxx) (Required): ")

    email = input("Email (optional, press Enter to skip): ")
    while email and not is_valid_email(email):
        email = input("Email (optional, press Enter to skip): ")

    address = input("Address (optional, press Enter to skip): ")
    return {'first_name': first_name, 'last_name': last_name,
            'phone': phone, 'email': email, 'address': address}


class PhoneBook:
    """
    Phone Book Manager
    """

    def __init__(self):
        """
        The constructor of PhoneBook with initialized contacts and options
        """
        self.contacts = {}  # uuid.UUID => Contact
        self.options = OPERATIONS
        self.option_table = PrettyTable()
        self.option_table.field_names = ["Option (Case-insensitive)",
                                         "Description"]
        for option, description in self.options.items():
            self.option_table.add_row([option, description])

    def add_contact(self, contact_dict, from_file=False):
        """
        Add a contact to the phone book
        :param contact_dict: a given contact dict
        :param from_file: a boolean flag indicating if the contact is from a csv file
        :return: None
        """
        contact = Contact(contact_dict, is_new=True, from_file=from_file)
        self.contacts[contact.guid] = contact
        logger.warning(contact.guid)

    def search_contact(self):
        """
        Fuzzy search a contact
        :return: None
        """
        fuzzy_input = input("Please provide the contact you want to query:")
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
        best_match = process.extractOne(fuzzy_input, contact_details)
        best_match_contact = None
        if best_match:
            matched_index = contact_details.index(best_match[0])
            logger.warning(contact_list[matched_index].guid)
            best_match_contact = contact_list[matched_index]
        if best_match_contact is not None:
            print(best_match_contact)
        else:
            print('No contact found!')

    def get_contact_by_id(self, guid):
        """
        Get a contact with a given uuid
        :param guid: uuid.UUID string
        :return: a contact
        """
        for _, contact in self.contacts.items():
            if uuid.UUID(guid) == contact.guid and not contact.is_deleted():
                return contact

        return None

    def update_contact(self):
        """
        Update a contact based on a given guid
        :return: None
        """
        guid = ''
        while not is_valid_uuid(guid):
            guid = input("Please provide a valid contact ID:")

        contact = self.get_contact_by_id(guid)
        if contact is None:
            print("No contact found!")
        else:
            print(contact)
            new_first_name = ''
            while not new_first_name.strip():
                new_first_name = input(
                    f'First Name: [{contact.first_name}] (Required, press Enter to skip)')
                if not new_first_name.strip():
                    new_first_name = contact.first_name

            new_last_name = ''
            while not new_last_name.strip():
                new_last_name = input(
                    f'Last Name: [{contact.last_name}] (Required, press Enter to skip)')
                if not new_last_name.strip():
                    new_last_name = contact.last_name

            new_phone = ''
            while not new_phone.strip():
                new_phone = input(
                    f'Phone: [{contact.phone}] (Required, press Enter to skip)')
                if not new_phone.strip():
                    new_phone = contact.phone

            new_email = input(
                f'Email: [{contact.email}] (Optional, press Enter to skip or enter space to remove)')
            new_email = contact.email if not new_email.strip() else new_email
            while new_email and new_email.strip() and not is_valid_email(
                    new_email):
                new_email = input(
                    f'Email: [{contact.email}] (Optional, press Enter to skip or enter space to remove)')
                if not new_email:
                    new_email = contact.address
                elif not new_email.strip():
                    new_email = ''
                    break

            new_address = input(
                f'Address: [{contact.address}] (Optional, press Enter to skip or enter space to remove)')
            if not new_address:
                new_address = contact.address
            elif not new_address.strip():
                new_address = new_address.strip()

            self.contacts[contact.guid] = Contact({
                "guid": contact.guid,
                "first_name": new_first_name,
                "last_name": new_last_name,
                "phone": new_phone,
                "email": new_email,
                "address": new_address,
            }, is_new=False)
            logger.warning(contact.guid)
            print(self.contacts[contact.guid])

    def delete_contact(self):
        """
        Delete a contact
        :return: None
        """
        if count_contacts(self.contacts):
            guid = input("Please provide a valid contact ID:")
            if is_valid_uuid(guid):
                contact = self.get_contact_by_id(guid)
                if contact is not None:
                    print(contact)
                    confirmation_answer = 'Yn'
                    while confirmation_answer != 'Y' and confirmation_answer != 'n' and confirmation_answer != '':
                        confirmation_answer = input(
                            'Delete this contact? [Y/n(Default)]')
                    if confirmation_answer == 'Y':
                        contact.delete()
                        logger.warning(contact.guid)
                        print('The contact was deleted!')
                    else:
                        print('The deletion was canceled!')
                else:
                    print('No contact found!')
            else:
                print("Invalid ID:", guid)
        else:
            print('No contact can be found for deletion!')
