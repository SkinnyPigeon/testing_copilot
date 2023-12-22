import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Base
from database_functions import (
    create_session,
    create_user_table,
    create_user,
    check_user_credentials,
)


def test_create_session():
    session = create_session()
    assert session is not None


def test_create_user_table():
    engine = create_engine("sqlite:///:memory:")
    create_user_table(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    session.query(User).first()


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    create_user_table(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)


@pytest.fixture
def patched_create_session(monkeypatch, session):
    monkeypatch.setattr("database_functions.create_session", lambda: session)


def test_create_user(patched_create_session):
    result, message = create_user("testuser", "test@example.com", "testpassword")
    assert result is True
    assert message == "User created successfully"


def test_create_duplicate_user(patched_create_session):
    create_user("testuser", "test@example.com", "testpassword")
    result, message = create_user("testuser", "test@example.com", "testpassword")
    assert result is False
    assert message == "Your email has already been registered"


def test_check_user_credentials(patched_create_session):
    create_user("testuser", "test@example.com", "testpassword")
    result, message = check_user_credentials("test@example.com", "testpassword")
    assert result is True
    assert message == "User credentials are correct"


def test_check_user_incorrect_credentials(patched_create_session, session):
    create_user("testuser", "test@example.com", "testpassword")
    result, message = check_user_credentials("test@example.com", "wrongpassword")
    assert result is False
    assert message == "User credentials are incorrect"
