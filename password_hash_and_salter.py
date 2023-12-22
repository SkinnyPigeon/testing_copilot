"""Salts and Hashes a password for storage in the database."""

import bcrypt


def hash_password(password: str):
    """Hashes a password using bcrypt.

    Parameters:
        password (str): The password to be hashed.

    Returns:
        hashed_password (str): The hashed password."""
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed.decode("utf-8")


def check_password(password: str, hashed: str):
    """Checks a password against a hash using bcrypt.

    Parameters:
        password (str): The password to be checked.
        hashed (str): The hash to check the password against.

    Returns:
        match (bool): Whether the password matches the hash."""
    password = password.encode()
    if bcrypt.checkpw(password, hashed):
        return True
    else:
        return False
