
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db
import asyncio

DATABASE_URL_TEST = "sqlite+aiosqlite:///:memory:"

engine_test = create_async_engine(DATABASE_URL_TEST, echo=False)
TestSessionLocal = sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="function", autouse=True)
async def override_get_db():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async def _get_db():
        async with TestSessionLocal() as session:
            yield session
    app.dependency_overrides[get_db] = _get_db
