import uuid


def is_valid_uuid(uuid_str: str):
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False


def is_valid_phone_number():
    pass


def is_valid_email():
    pass
