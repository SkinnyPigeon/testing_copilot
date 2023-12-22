import pytest
from models import User
from sqlalchemy.exc import IntegrityError, StatementError

def test_create_user(session):
    user = User(username="testuser", email="test@example.com", password="testpassword")
    session.add(user)
    session.commit()
    assert user.id is not None

def test_missing_fields(session):
    with pytest.raises(IntegrityError):
        user = User()
        session.add(user)
        session.commit()

def test_unique_email(session):
    user1 = User(username="testuser1", email="test@example.com", password="testpassword1")
    session.add(user1)
    session.commit()
    with pytest.raises(IntegrityError):
        user2 = User(username="testuser2", email="test@example.com", password="testpassword2")
        session.add(user2)
        session.commit()

def test_incorrect_field_type(session):
    user = User(username=123, email="test@example.com", password="testpassword")
    session.add(user)
    session.commit()
    assert isinstance(user.username, str)
