import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.db.mongodb import init_db, close_db, get_database
from app.db.seed import seed_database

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    await init_db()
    db = get_database()
    await seed_database(db)
    yield
    await close_db()

@pytest.mark.asyncio
async def test_progressive_hint_system_and_attempt_tracking():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register user
        reg_res = await client.post("/api/auth/register", json={
            "name": "Devin Coder",
            "email": "devin.coder@test.com",
            "password": "Password123!",
            "languages": ["python"],
            "self_declared_level": "beginner"
        })
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create session for factorial problem
        sess_res = await client.post("/api/sessions", json={"problem_id": "prob_recursion_factorial"}, headers=headers)
        assert sess_res.status_code == 201
        session_id = sess_res.json()["id"]

        # ATTEMPT 1: Incorrect code with missing base case
        wrong_code_1 = "def factorial(n):\n    return n * factorial(n - 1)\n"
        att1_res = await client.post(f"/api/sessions/{session_id}/attempt", json={"code": wrong_code_1}, headers=headers)
        assert att1_res.status_code == 200
        data1 = att1_res.json()
        assert data1["is_correct"] is False
        assert data1["attempt_number"] == 1
        assert data1["attempts_remaining"] == 2
        assert data1["hint_level"] == 1
        assert data1["solution_unlocked"] is False
        assert data1["solution"] is None  # Strictly locked!
        assert data1["error_type"] in ["RUNTIME_ERROR", "LOGICAL_ERROR"]
        assert "base_case" in (data1["misconception"] or "") or "recursion" in data1["concept"]

        # ATTEMPT 2: Still incorrect (wrong step)
        wrong_code_2 = "def factorial(n):\n    if n == 0: return 0\n    return n * factorial(n - 1)\n"
        att2_res = await client.post(f"/api/sessions/{session_id}/attempt", json={"code": wrong_code_2}, headers=headers)
        assert att2_res.status_code == 200
        data2 = att2_res.json()
        assert data2["is_correct"] is False
        assert data2["attempt_number"] == 2
        assert data2["attempts_remaining"] == 1
        assert data2["hint_level"] == 2
        assert data2["solution_unlocked"] is False
        assert data2["solution"] is None  # Still locked!

        # ATTEMPT 3: Final failed attempt -> Triggers Solution Unlock!
        wrong_code_3 = "def factorial(n):\n    return 1\n"
        att3_res = await client.post(f"/api/sessions/{session_id}/attempt", json={"code": wrong_code_3}, headers=headers)
        assert att3_res.status_code == 200
        data3 = att3_res.json()
        assert data3["attempt_number"] == 3
        assert data3["attempts_remaining"] == 0
        assert data3["solution_unlocked"] is True
        assert data3["solution"] is not None  # Now unlocked!
        assert "def factorial" in data3["solution"]
