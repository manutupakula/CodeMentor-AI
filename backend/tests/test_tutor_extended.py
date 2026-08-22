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
async def test_unauthorized_session_access():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # User 1
        u1_res = await client.post("/api/auth/register", json={
            "name": "User One", "email": "user1@test.com", "password": "Password123!"
        })
        t1 = u1_res.json()["access_token"]

        # User 2
        u2_res = await client.post("/api/auth/register", json={
            "name": "User Two", "email": "user2@test.com", "password": "Password123!"
        })
        t2 = u2_res.json()["access_token"]

        # User 1 creates session
        sess = await client.post("/api/sessions", json={"problem_id": "prob_recursion_factorial"}, headers={"Authorization": f"Bearer {t1}"})
        sess_id = sess.json()["id"]

        # User 2 tries to access or submit to User 1's session -> MUST be 403 Forbidden
        u2_attempt = await client.post(
            f"/api/sessions/{sess_id}/attempt",
            json={"code": "def factorial(n): return 1"},
            headers={"Authorization": f"Bearer {t2}"}
        )
        assert u2_attempt.status_code == 403

        u2_sess_get = await client.get(f"/api/sessions/{sess_id}", headers={"Authorization": f"Bearer {t2}"})
        assert u2_sess_get.status_code == 403

@pytest.mark.asyncio
async def test_custom_problem_analysis():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        reg_res = await client.post("/api/auth/register", json={
            "name": "Custom Problem User", "email": "custom@test.com", "password": "Password123!"
        })
        t = reg_res.json()["access_token"]

        custom_payload = {
            "problem_title": "Find Maximum in List",
            "problem_description": "Return the maximum element in a list of numbers.",
            "student_code": "def find_max(nums):\n    m = 0\n    for x in nums:\n        if x > m: m = x\n    return m\n",
            "hint_level": 1
        }
        res = await client.post("/api/tutor/custom-problem", json=custom_payload, headers={"Authorization": f"Bearer {t}"})
        assert res.status_code == 200
        data = res.json()
        assert "hint" in data
        assert data["hint_level"] == 1
        assert "analysis" in data

@pytest.mark.asyncio
async def test_revise_mistakes_endpoint():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        reg_res = await client.post("/api/auth/register", json={
            "name": "Revision User", "email": "revise@test.com", "password": "Password123!"
        })
        t = reg_res.json()["access_token"]

        # Create session and make incorrect attempt to generate mistake
        sess = await client.post("/api/sessions", json={"problem_id": "prob_recursion_factorial"}, headers={"Authorization": f"Bearer {t}"})
        sess_id = sess.json()["id"]
        
        # Wrong code without base case
        await client.post(f"/api/sessions/{sess_id}/attempt", json={"code": "def factorial(n): return n * factorial(n - 1)"}, headers={"Authorization": f"Bearer {t}"})

        # Fetch revision mistakes
        rev_res = await client.get("/api/learner/revise-mistakes", headers={"Authorization": f"Bearer {t}"})
        assert rev_res.status_code == 200
        revs = rev_res.json()
        assert len(revs) > 0
        assert "missing base case" in revs[0]["mistake_type"].lower()
        assert revs[0]["count"] >= 1
