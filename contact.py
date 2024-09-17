import uuid

from prettytable import PrettyTable


class Contact:
    def __init__(self, d):
        self.guid = uuid.uuid4()
        self.first_name = d['first_name'] if 'first_name' in d else ''
        self.last_name = d['last_name'] if 'last_name' in d else ''
        self.phone = d['phone'] if 'phone' in d else ''
        self.email = d['email'] if 'email' in d else ''
        self.address = d['address'] if 'address' in d else ''

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
