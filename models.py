"""
This module defines the SQLAlchemy ORM model for the 'users' table.

Model:
- User: Used for registering new users and authenticating existing ones during login.

The model uses SQLAlchemy's declarative base and supports automatic timestamping.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_technical = Column(Boolean, default=False)
