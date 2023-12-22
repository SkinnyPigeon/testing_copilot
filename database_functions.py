# Handles the database functions for the application.
# Uses sqlalchemy to handle the connection to a postgres database.
# Pydantic Basemodel is defined in models.py

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from models import User
from password_hash_and_salter import hash_password, check_password


def create_session():
    """Creates a session to the database.

    Returns:
        session: A session to the database."""
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()


def create_user_table(engine):
    """Creates the user table in the database."""
    with create_session() as _:
        User.metadata.create_all(engine)


def create_user(username, email, password):
    """Creates a user in the database.

    Parameters:
        username (str): The username of the user.
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        bool: Whether the user was created successfully.
        str: A message about the result of the operation.
    """
    with create_session() as session:
        user = User(username=username, email=email, password=hash_password(password))
        try:
            session.add(user)
            session.commit()
            return True, "User created successfully"
        except IntegrityError:
            session.rollback()
            return False, "Your email has already been registered"


def check_user_credentials(email, password):
    """Checks the credentials of a user.

    Parameters:
        email (str): The email of the user.
        password (str): The password of the user.

    Returns:
        bool: Whether the user was created successfully.
        str: A message about the result of the operation.
    """
    with create_session() as session:
        user = session.query(User).filter(User.email == email).first()
        if user:
            try:
                check_password(password, user.password.encode())
                return True, "User credentials are correct"
            except ValueError:
                return False, "User credentials are incorrect"
        else:
            return False, "User credentials are incorrect"


def display_results_of_create_user(result, message):
    """Displays the results of the create_user function.

    Parameters:
        result (bool): Whether the user was created successfully.
        message (str): A message about the result of the operation.
    """
    if result:
        print("Woohoo! User created")
        print(message)
    else:
        print("Oh no! User not created")
        print(message)


def display_results_of_check_user_credentials(result, message):
    """Displays the results of the check_user_credentials function.

    Parameters:
        result (bool): Whether the user was created successfully.
        message (str): A message about the result of the operation.
    """
    if result:
        print("Woohoo! User credentials are correct")
        print(message)
    else:
        print("Oh no! User credentials are incorrect")
        print(message)


create_user_table(create_engine(os.environ["DATABASE_URL"]))
result, message = create_user("me", "me@me.com", "password")
display_results_of_create_user(result, message)
result, message = create_user("me", "me2@me.com", "password")
display_results_of_create_user(result, message)


result, message = check_user_credentials("me3@me.com", "password")
display_results_of_check_user_credentials(result, message)
result, message = check_user_credentials("me@me.com", "password")
display_results_of_check_user_credentials(result, message)
