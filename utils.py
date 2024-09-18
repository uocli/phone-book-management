import re
import uuid

from email_validator import validate_email, EmailNotValidError


def is_valid_uuid(uuid_str: str):
    """
    Validate a given uuid string
    :param uuid_str: uuid string
    :return: True if the uuid string is a valid uuid, False otherwise
    """
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False


def is_valid_phone_number(phone_number):
    """
    Validate a given phone number, in this case the only accepted format is (xxx) xxx-xxxx.
    :param phone_number: the given phone number string
    :return: True if the phone number is valid, False otherwise
    """
    match = re.search('^\(\d{3}\)\s\d{3}-\d{4}$', phone_number)
    # (123) 456-7890
    if match:
        return True
    return False


def is_valid_email(email):
    """
    Validate a given Email address
    :param email: email address string
    :return: True if the given email is valid, False otherwise
    """
    try:
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False


def is_valid_date(date_str):
    """
    Validate a given date string
    :param date_str: the date string
    :return: True if the given date string is valid, False otherwise
    """
    match = re.search('^\d{4}-\d{2}-\d{2}$', date_str)
    # 2024-05-06
    if match:
        return True
    return False
