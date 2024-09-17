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
            print('You are creating a new contact!')
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            phone = input("Phone: ")
            email = input("Email (optional, press Enter to skip): ")
            address = input("Address (optional, press Enter to skip): ")
            phonebook.add_contact(first_name, last_name, phone, email, address)
        elif option == 'L':
            phonebook.list_contacts()
        elif option == 'E':
            print("Goodbye!")
            sys.exit()
        else:
            print("Only these options are available, please try again!")
            print(option_table)


if __name__ == "__main__":
    main()
