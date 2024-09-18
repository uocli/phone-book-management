import csv
import sys

from prettytable import PrettyTable

from contact import Contact
from phonebook import PhoneBook, list_contacts, count_contacts, delete_contact, \
    create_contact_dict
from utils import is_valid_uuid, is_valid_email, \
    sorted_contact, is_valid_date
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
            contact_dict = create_contact_dict()
            phonebook.add_contact(contact_dict)
        elif option == 'L':
            # Listing all contacts
            list_contacts(phonebook.contacts)
        elif option == 'Q':
            # Fuzzy querying a contact
            fuzzy_input = input("Please provide the contact you want to query:")
            best_match = phonebook.search_contact(fuzzy_input)
            print(best_match)
        elif option == 'D':
            # Soft-deleting a contact
            if count_contacts(phonebook.contacts):
                guid = input("Please provide a valid contact ID:")
                if is_valid_uuid(guid):
                    contact = phonebook.get_contact_by_id(guid)
                    if contact is not None:
                        print(contact)
                        confirmation_answer = 'Yn'
                        while confirmation_answer != 'Y' and confirmation_answer != 'n' and confirmation_answer != '':
                            confirmation_answer = input(
                                'Delete this contact? [Y/n(Default)]')
                        if confirmation_answer == 'Y':
                            delete_contact(contact)
                            print('The contact was deleted!')
                        else:
                            print('The deletion was canceled!')
                    else:
                        print('No contact found!')
                else:
                    print("Invalid ID:", guid)
            else:
                print('No contact can be found for deletion!')
        elif option == 'E':
            # Exiting the system
            print("Goodbye!")
            sys.exit()
        elif option == 'LA' or option == 'LD':
            # Sorting contacts in ascending (LA) or descending (LD) order
            list_contacts(sorted_contact(phonebook.contacts,
                                         True if option == 'LD' else False))
        elif option == 'LF':
            # Listing with filters
            start_date = ''
            end_date = ''
            while not is_valid_date(start_date):
                start_date = input('Please specify a start date (yyyy-MM-dd)')

            while not is_valid_date(end_date):
                end_date = input('Please specify an end date (yyyy-MM-dd)')

            list_contacts(phonebook.contacts, start_date, end_date)
        elif option == 'F':
            # Reading a list contacts from a csv file
            path = input("Please provide a complete csv file path:")
            try:
                with open(path) as csv_file:
                    reader = csv.DictReader(csv_file)
                    for row in reader:
                        phonebook.add_contact(row, from_file=True)
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
                    if not new_first_name.strip():
                        new_first_name = contact.first_name

                while not new_last_name.strip():
                    new_last_name = input(
                        f'Last Name: [{contact.last_name}] (Required, press Enter to skip)')
                    if not new_last_name.strip():
                        new_last_name = contact.last_name

                while not new_phone.strip():
                    new_phone = input(
                        f'Phone: [{contact.phone}] (Required, press Enter to skip)')
                    if not new_phone.strip():
                        new_phone = contact.phone

                new_email = input(
                    f'Email: [{contact.email}] (Optional, press Enter to skip or enter space to remove)')
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
