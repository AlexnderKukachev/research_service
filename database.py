"""
This module initializes database engines for MongoDB and PostgreSQL.

- Creates an asynchronous MongoDB client using Motor.
- Initializes an asynchronous SQLAlchemy engine for PostgreSQL.
- Defines a session factory for database operations using SQLAlchemy's AsyncSession.
- Provides a dependency function `get_db` to be used with FastAPI for handling PostgreSQL sessions in an async context.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import config

# MongoDB setup
mongo_client = AsyncIOMotorClient(config.MONGODB_URI)
mongo_db = mongo_client[config.DB_NAME]

# PostgreSQL setup with SQLAlchemy Async
engine = create_async_engine(config.POSTGRES_URI, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
