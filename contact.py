import uuid

from prettytable import PrettyTable


class Contact:
    def __init__(self, first_name, last_name, phone, email, address):
        self.guid = uuid.uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address = address

    def __init__(self, d):
        for key, value in d.items():
            self.guid = uuid.uuid4()
            setattr(self, key, value)

    def __str__(self):
        contact_table = PrettyTable()
        contact_table.field_names = ["First Name", "Last Name", 'Phone',
                                     'Email', 'Address']
        contact_table.add_row([
            self.first_name,
            self.last_name,
            self.phone,
            self.email,
            self.address
        ])
        # f'First Name: {self.first_name}, Last Name: {self.last_name}, Phone: {self.phone}, Email: {self.email}, Address: {self.address}'
        return contact_table.get_string()
