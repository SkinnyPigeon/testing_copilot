"""This module contains functions for interacting with the database."""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.engine.base import Engine
from models import User
from password_hash_and_salter import hash_password, check_password


def create_session() -> sessionmaker:
    """Creates a session to the database.

    Returns:
        session: A session to the database."""
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    return Session()


def create_user_table(engine: Engine) -> None:
    """Creates the user table in the database."""
    with create_session() as _:
        User.metadata.create_all(engine)


def create_user(username: str, email: str, password: str) -> (bool, str):
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


def check_user_credentials(email: str, password: str) -> (bool, str):
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


messages = {
    "user_created": {
        True: "Woohoo! User created",
        False: "Oh no! User not created",
    },
    "user_credentials": {
        True: "Woohoo! User credentials are correct",
        False: "Oh no! User credentials are incorrect",
    },
}


def display_results(result: bool, message: str, interaction: str) -> None:
    """Displays the results of the database interaction.

    Parameters:
        result (bool): Whether the interaction was successful.
        message (str): A message about the result of the interaction.
    """
    if result:
        print(messages[interaction][True])
        print(message)
    else:
        print(messages[interaction][False])
        print(message)


create_user_table(create_engine(os.environ["DATABASE_URL"]))
result, message = create_user("me", "me@me.com", "password")
display_results(result, message, "user_created")
result, message = create_user("me", "me2@me.com", "password")
display_results(result, message, "user_created")


result, message = check_user_credentials("me3@me.com", "password")
display_results(result, message, "user_credentials")
result, message = check_user_credentials("me@me.com", "password")
display_results(result, message, "user_credentials")
