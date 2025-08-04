import pytest
from httpx import AsyncClient, ASGITransport
from main import app

@pytest.mark.anyio
async def test_sample_crud_flow():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post("/register", json={"username": "sampleuser", "password": "123456"})
        login = await ac.post("/login", data={"username": "sampleuser", "password": "123456"})
        token = login.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}
        # Create sample
        sample_data = {
            "sample_type": "blood",
            "subject_id": "001",
            "collection_date": "2021-01-01",
            "status": "collected",
            "storage_location": "FRZ01"
        }
        create = await ac.post("/samples", json=sample_data, headers=headers)
        assert create.status_code == 201
        sample_id = create.json()["sample_id"]

        # Get sample
        get = await ac.get(f"/samples/{sample_id}", headers=headers)
        assert get.status_code == 200
        assert get.json()["subject_id"] == "001"
