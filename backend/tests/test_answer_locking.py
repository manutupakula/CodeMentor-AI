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
async def test_server_side_answer_locking_enforcement():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register user
        reg_res = await client.post("/api/auth/register", json={
            "name": "Lock Test User",
            "email": "lock.user@test.com",
            "password": "Password123!",
            "languages": ["python"],
            "self_declared_level": "intermediate"
        })
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Create session
        sess_res = await client.post("/api/sessions", json={"problem_id": "prob_recursion_factorial"}, headers=headers)
        session_id = sess_res.json()["id"]

        # 1. Attempt to fetch solution immediately -> MUST BE 403 Forbidden!
        locked_res = await client.get(f"/api/sessions/{session_id}/solution", headers=headers)
        assert locked_res.status_code == 403
        assert "locked" in locked_res.json()["detail"].lower()

        # 2. Make 1 incorrect attempt
        wrong_code = "def factorial(n): return -1"
        await client.post(f"/api/sessions/{session_id}/attempt", json={"code": wrong_code}, headers=headers)

        # 3. Attempt to fetch solution after 1 attempt -> STILL 403 Forbidden!
        locked_res_2 = await client.get(f"/api/sessions/{session_id}/solution", headers=headers)
        assert locked_res_2.status_code == 403

        # 4. Correct solution unlocks immediately
        correct_code = "def factorial(n):\n    if n <= 1: return 1\n    return n * factorial(n - 1)"
        solve_res = await client.post(f"/api/sessions/{session_id}/attempt", json={"code": correct_code}, headers=headers)
        assert solve_res.json()["is_correct"] is True
        assert solve_res.json()["solution_unlocked"] is True

        # 5. Now solution endpoint returns 200 OK
        unlocked_res = await client.get(f"/api/sessions/{session_id}/solution", headers=headers)
        assert unlocked_res.status_code == 200
        assert "def factorial" in unlocked_res.json()["solution"]
