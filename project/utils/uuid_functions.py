import uuid


def is_valid_uuid(val):
    """Check UUID validity in Python?"""
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False
