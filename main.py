import csv
import sys

from phonebook import PhoneBook, list_contacts, create_contact_dict, \
    sorting_contact
from utils import is_valid_date
from custom_logger import logger


def main():
    print("\nWelcome to the Phone Book Management App!")
    logger.info('System started')
    phonebook = PhoneBook()
    print(phonebook.option_table)
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
            phonebook.search_contact()
        elif option == 'D':
            # Soft-deleting a contact
            phonebook.delete_contact()
        elif option == 'E':
            # Exiting the system
            print("Goodbye!")
            sys.exit()
        elif option == 'LA' or option == 'LD':
            # Sorting contacts in ascending (LA) or descending (LD) order
            sorted_contact_dict = sorting_contact(phonebook.contacts,
                                                  desc=True if option == 'LD' else False)
            list_contacts(sorted_contact_dict)
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
            phonebook.update_contact()
        else:
            # Getting an invalid operation
            print("Only these options are available, please try again!")
            print(phonebook.option_table)


if __name__ == "__main__":
    main()
