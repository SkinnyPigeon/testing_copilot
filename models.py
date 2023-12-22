"""Uses SQLAlchemy to create ORM models for the database."""

from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

if TYPE_CHECKING:
    from sqlalchemy.ext.declarative import DeclarativeMeta as Base
else:
    Base = declarative_base()


class User(Base):
    """A user of the application."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
