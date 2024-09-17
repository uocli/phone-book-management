import uuid


class Contact:
    def __init__(self, first_name, last_name, phone, email, address):
        self.guid = uuid.uuid4()
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.address = address