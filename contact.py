import uuid
from datetime import datetime

from prettytable import PrettyTable

from utils import is_valid_date


class Contact:
    def __init__(self, d: dict, is_new=True, from_file=False):
        self.guid = uuid.uuid4() if is_new else d['guid']
        self.first_name = d['first_name'] if 'first_name' in d else ''
        self.last_name = d['last_name'] if 'last_name' in d else ''
        self.phone = d['phone'] if 'phone' in d else ''
        self.email = d['email'] if 'email' in d else ''
        self.address = d['address'] if 'address' in d else ''
        self._is_deleted = False
        self.__created_date = datetime.strptime(d["created_date"],
                                                '%Y-%m-%d').date() \
            if from_file and d["created_date"] and \
               is_valid_date(d["created_date"]) else datetime.now().date()

    def created_date(self):
        return self.__created_date

    def delete(self):
        self._is_deleted = True

    def is_deleted(self):
        return self._is_deleted == True

    def __str__(self):
        contact_table = PrettyTable()
        contact_table.field_names = ["ID", "First Name", "Last Name", 'Phone',
                                     'Email', 'Address', "Created Date"]
        contact_table.add_row([
            self.guid,
            self.first_name,
            self.last_name,
            self.phone,
            self.email,
            self.address,
            self.__created_date
        ])
        # f'First Name: {self.first_name}, Last Name: {self.last_name}, Phone: {self.phone}, Email: {self.email}, Address: {self.address}'
        return contact_table.get_string()
