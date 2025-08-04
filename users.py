"""
User model for interacting with the 'users' table in the database.

The User class defines the schema of the users table used by SQLAlchemy ORM.
Each record contains a username and its associated hashed password.

Fields:
- username (str): the user's name, serves as the primary key.
- hashed_password (str): the user's hashed password, required.

This model is used for user registration and authentication.
"""

from sqlalchemy import Column, String
from database import Base

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String, nullable=False)