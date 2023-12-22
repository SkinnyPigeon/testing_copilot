import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

@pytest.fixture(scope='function')
def session():
    engine = create_engine('sqlite:///:memory:')  # Use an in-memory SQLite database for tests
    Base.metadata.create_all(engine)  # Create the tables
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session  # This is where the testing happens
    session.rollback()  # Roll back any changes made during the tests
    session.close()  # Close the session
    Base.metadata.drop_all(engine)  # Drop the tables