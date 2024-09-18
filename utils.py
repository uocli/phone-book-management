import re
import uuid


def is_valid_uuid(uuid_str: str):
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False


def is_valid_phone_number(phone_number):
    match = re.search('^\(\d{3}\)\s\d{3}-\d{4}$', phone_number)
    # (123) 456-7890
    if match:
        return True
    return False


def is_valid_email():
    pass
