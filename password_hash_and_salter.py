# Salts and Hashes a password for storage in the database.

import bcrypt
from dotenv import load_dotenv

load_dotenv()


def hash_password(password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed.decode("utf-8")


def check_password(password, hashed):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    password = password.encode()
    if bcrypt.checkpw(password, hashed):
        return True
    else:
        return False
