import re
import uuid

from email_validator import validate_email, EmailNotValidError


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


def is_valid_email(email):
    try:
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError as e:
        return False


def is_valid_date(date_str):
    match = re.search('^\d{4}-\d{2}-\d{2}$', date_str)
    # 2024-05-06
    if match:
        return True
    return False



