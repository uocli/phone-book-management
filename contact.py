import uuid
from datetime import datetime

from prettytable import PrettyTable


class Contact:
    def __init__(self, d: dict, is_new=True):
        self.guid = uuid.uuid4() if is_new else d['guid']
        self.first_name = d['first_name'] if 'first_name' in d else ''
        self.last_name = d['last_name'] if 'last_name' in d else ''
        self.phone = d['phone'] if 'phone' in d else ''
        self.email = d['email'] if 'email' in d else ''
        self.address = d['address'] if 'address' in d else ''
        self._is_deleted = False
        self.__created_at = datetime.now()

    def delete(self):
        self._is_deleted = True

    def is_deleted(self):
        return self._is_deleted == True

    def __str__(self):
        contact_table = PrettyTable()
        contact_table.field_names = ["ID", "First Name", "Last Name", 'Phone',
                                     'Email', 'Address']
        contact_table.add_row([
            self.guid,
            self.first_name,
            self.last_name,
            self.phone,
            self.email,
            self.address
        ])
        # f'First Name: {self.first_name}, Last Name: {self.last_name}, Phone: {self.phone}, Email: {self.email}, Address: {self.address}'
        return contact_table.get_string()
