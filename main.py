import csv
import sys

from prettytable import PrettyTable

from phonebook import PhoneBook


def main():
    print("\nWelcome to the Phone Book Management App!")
    phonebook = PhoneBook()
    option_table = PrettyTable()
    option_table.field_names = ["Option (Case-insensitive)", "Description"]
    for option, description in phonebook.options.items():
        option_table.add_row([option, description])
    print(option_table)
    while True:
        option = input("Choose an option (C,R,U,D or E): ")
        option = option.upper()
        if option == 'C':
            # Creating a new contact manually
            print('You are creating a new contact!')
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            phone = input("Phone: ")
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
        else:
            # Getting an invalid operation
            print("Only these options are available, please try again!")
            print(option_table)


if __name__ == "__main__":
    main()
