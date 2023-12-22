"""Tests for password_hash_and_salter.py"""

from password_hash_and_salter import hash_password, check_password


def test_hash_password():
    """Tests that the hash_password function returns a string and that the string is not the same as the input."""
    password = "my_password"
    hashed_password = hash_password(password)
    assert isinstance(hashed_password, str)
    assert hashed_password != password


def test_check_password():
    """Tests that the check_password function returns True if the password matches the hash and False if it doesn't."""
    password = "my_password"
    hashed_password = hash_password(password)
    assert check_password(password, hashed_password.encode("utf-8")) is True
    assert check_password("wrong_password", hashed_password.encode("utf-8")) is False
