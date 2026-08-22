import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.mongodb import init_db, close_db

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    await init_db()
    yield
    await close_db()

@pytest.mark.asyncio
async def test_user_registration_and_login():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Register User
        reg_payload = {
            "name": "Alex Mercer",
            "email": "alex.mercer@test.com",
            "password": "Password123!",
            "languages": ["python"],
            "self_declared_level": "intermediate",
            "selected_topics": ["Loops", "Arrays", "Recursion"]
        }
        res = await client.post("/api/auth/register", json=reg_payload)
        assert res.status_code == 201, res.text
        data = res.json()
        assert "access_token" in data
        assert data["user"]["email"] == "alex.mercer@test.com"
        assert data["user"]["self_declared_level"] == "intermediate"
        token = data["access_token"]

        # 2. Get Current User (/me)
        me_res = await client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_res.status_code == 200
        assert me_res.json()["name"] == "Alex Mercer"

        # 3. Login
        login_res = await client.post("/api/auth/login", json={
            "email": "alex.mercer@test.com",
            "password": "Password123!"
        })
        assert login_res.status_code == 200
        assert "access_token" in login_res.json()

        # 4. Login with Wrong Password
        bad_login = await client.post("/api/auth/login", json={
            "email": "alex.mercer@test.com",
            "password": "WrongPassword"
        })
        assert bad_login.status_code == 401
