import csv
import sys

from prettytable import PrettyTable

from contact import Contact
from phonebook import PhoneBook
from utils import is_valid_uuid, is_valid_phone_number, is_valid_email
from custom_logger import logger


def main():
    print("\nWelcome to the Phone Book Management App!")
    logger.info('System started')
    phonebook = PhoneBook()
    option_table = PrettyTable()
    option_table.field_names = ["Option (Case-insensitive)", "Description"]
    for option, description in phonebook.options.items():
        option_table.add_row([option, description])
    print(option_table)
    while True:
        option = input("Choose an option: ")
        option = option.upper()
        logger.info(option)
        if option == 'C':
            # Creating a new contact manually
            print('You are creating a new contact!')
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
            contact_dict = {'first_name': first_name, 'last_name': last_name,
                            'phone': phone, 'email': email, 'address': address}
            phonebook.add_contact(contact_dict)
        elif option == 'L':
            # Listing all contacts
            phonebook.list_contacts()
        elif option == 'Q':
            # Fuzzy querying a contact
            fuzzy_input = input("Please provide the contact you want to query:")
            best_match = phonebook.search_contact(fuzzy_input)
            print(best_match)
        elif option == 'D':
            # Soft-deleting a contact
            if phonebook.count_contacts():
                guid = input("Please provide a valid contact ID:")
                if is_valid_uuid(guid):
                    contact = phonebook.get_contact_by_id(guid)
                    print(contact)
                    confirmation_answer = 'Yn'
                    while confirmation_answer != 'Y' and confirmation_answer != 'n' and confirmation_answer != '':
                        confirmation_answer = input(
                            'Delete this contact? [Y/n(Default)]')
                    if confirmation_answer == 'Y':
                        phonebook.delete_contact(contact)
                        print('The contact was deleted!')
                    else:
                        print('The deletion was canceled!')
                else:
                    print("Invalid ID:", guid)
            else:
                print('No contact can be found for deletion!')
        elif option == 'E':
            # Exiting the system
            print("Goodbye!")
            sys.exit()
        elif option == 'F':
            # Reading a list contacts from a csv file
            path = input("Please provide a complete csv file path:")
            try:
                with open(path) as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        phonebook.add_contact(row)
            except FileNotFoundError as e:
                print(e)
            except TypeError as e:
                print(e)
        elif option == 'U':
            # Updating a contact
            guid = ''
            while not is_valid_uuid(guid):
                guid = input("Please provide a valid contact ID:")

            contact = phonebook.get_contact_by_id(guid)
            if contact is None:
                print("No contact found!")
            else:
                print(contact)
                new_first_name = ''
                new_last_name = ''
                new_phone = ''
                while not new_first_name.strip():
                    new_first_name = input(
                        f'First Name: [{contact.first_name}] (Required, press Enter to skip)')
                    if not new_first_name:
                        new_first_name = contact.first_name

                while not new_last_name.strip():
                    new_last_name = input(
                        f'Last Name: [{contact.last_name}] (Required, press Enter to skip)')
                    if not new_last_name:
                        new_last_name = contact.last_name

                while not new_phone.strip():
                    new_phone = input(
                        f'Phone: [{contact.phone}] (Required, press Enter to skip)')
                    if not new_phone:
                        new_phone = contact.phone

                new_email = input(
                    f'Email: [{contact.email}] (Optional, press Enter to skip or enter space to remove)')
                if not new_email:
                    new_email = contact.address
                elif not new_email.strip():
                    new_email = new_email.strip()

                new_address = input(
                    f'Address: [{contact.address}] (Optional, press Enter to skip or enter space to remove)')
                if not new_address:
                    new_address = contact.address
                elif not new_address.strip():
                    new_address = new_address.strip()

                contact = Contact({
                    "guid": contact.guid,
                    "first_name": new_first_name,
                    "last_name": new_last_name,
                    "phone": new_phone,
                    "email": new_email,
                    "address": new_address,
                }, is_new=False)
                phonebook.update_contact(contact)
        else:
            # Getting an invalid operation
            print("Only these options are available, please try again!")
            print(option_table)


if __name__ == "__main__":
    main()
