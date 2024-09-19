import uuid
from datetime import datetime

from prettytable import PrettyTable

from utils import is_valid_date


class Contact:
    """
    Contact
    """

    def __init__(self, d: dict, is_new=True, from_file=False):
        self.guid = uuid.uuid4() if is_new else d['guid']
        self.first_name = d['first_name'] if 'first_name' in d else ''
        self.last_name = d['last_name'] if 'last_name' in d else ''
        self.phone = d['phone'] if 'phone' in d else ''
        self.email = d['email'] if 'email' in d else ''
        self.address = d['address'] if 'address' in d else ''
        self.__is_deleted = False
        self.__created_date = datetime.strptime(d["created_date"],
                                                '%Y-%m-%d').date() \
            if from_file and d["created_date"] and \
               is_valid_date(d["created_date"]) else datetime.now().date()

    def created_date(self):
        """
        Get the created date of the contact
        :return: datetime.datetime.date object
        """
        return self.__created_date

    def delete(self):
        """
        Soft-delete a contact itself
        :return: None
        """
        self.__is_deleted = True

    def is_deleted(self):
        """
        Get the deletion status of a contact
        :return: True if the contact has been deleted, False otherwise
        """
        return self.__is_deleted == True

    def __str__(self):
        """
        Reformat the output of a contact
        :return: a formatted contact string
        """
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
        return contact_table.get_string()
