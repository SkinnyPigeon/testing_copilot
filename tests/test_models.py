"""Test models.py"""

import pytest
from models import User, Base
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="function")
def session():
    """Creates a session to an in-memory database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)


def test_create_user(session):
    """Tests that a user can be created."""
    user = User(username="testuser", email="test@example.com", password="testpassword")
    session.add(user)
    session.commit()
    assert user.id is not None


def test_missing_fields(session):
    """Tests that an IntegrityError is raised if a required field is missing."""
    with pytest.raises(IntegrityError):
        user = User()
        session.add(user)
        session.commit()


def test_unique_email(session):
    """Tests that an IntegrityError is raised if a user with the same email already exists."""
    user1 = User(
        username="testuser1", email="test@example.com", password="testpassword1"
    )
    session.add(user1)
    session.commit()
    with pytest.raises(IntegrityError):
        user2 = User(
            username="testuser2", email="test@example.com", password="testpassword2"
        )
        session.add(user2)
        session.commit()
