import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.anyio
async def test_register_and_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Register user
        response = await ac.post("/register", json={
            "username": "testuser",
            "password": "testpass"
        })
        assert response.status_code == 200
        assert response.json()["username"] == "testuser"

        # Login user
        response = await ac.post("/login", data={
            "username": "testuser",
            "password": "testpass"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()
