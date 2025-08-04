"""
This module defines Pydantic models used for request validation and response formatting
across all API endpoints in the FastAPI application.

It includes schemas for:
- Authentication (Token model).
- Sample management (Sample, SampleCreate, SampleUpdate).
- User registration and response formatting (UserCreate, UserOut).

These models ensure data consistency, validation, and serialization between the client and server.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional
import uuid
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str

class Sample(BaseModel):
    sample_id: str
    sample_type: Literal['blood', 'saliva', 'tissue']
    subject_id: str
    collection_date: datetime
    status: Literal['collected', 'processing', 'archived']
    storage_location: str

class SampleCreate(Sample):
    sample_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="UUID identifier")
    sample_type: Literal['blood', 'saliva', 'tissue']
    subject_id: str
    collection_date: datetime
    status: Literal['collected', 'processing', 'archived']
    storage_location: str

class SampleUpdate(BaseModel):
    sample_type: Optional[Literal['blood', 'saliva', 'tissue']]
    subject_id: Optional[str]
    collection_date: Optional[datetime]
    status: Optional[Literal['collected', 'processing', 'archived']]
    storage_location: Optional[str]

class UserCreate(BaseModel):
    username: str
    password: str
    is_technical: Optional[bool] = False  # можно указать при регистрации

class UserOut(BaseModel):
    id: int
    username: str
    created_at: datetime
    is_technical: bool

    model_config = ConfigDict(from_attributes=True)