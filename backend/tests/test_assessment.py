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
async def test_knowledge_check_flow_and_deterministic_scoring():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # Register user
        reg_res = await client.post("/api/auth/register", json={
            "name": "Jordan Lee",
            "email": "jordan.lee@test.com",
            "password": "Password123!",
            "languages": ["python"],
            "self_declared_level": "intermediate",
            "selected_topics": ["Loops", "Arrays"]
        })
        token = reg_res.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Start assessment
        start_res = await client.post("/api/assessment/start", headers=headers)
        assert start_res.status_code == 200
        start_data = start_res.json()
        questions = start_data["questions"]
        assert len(questions) > 0

        # Verify correct answers are hidden from the student
        for q in questions:
            assert "correct_answer" not in q
            assert "explanation" not in q

        # Submit answers: loops correct (10), arrays correct (O(1)), recursion wrong (answer B)
        answers = [
            {"question_id": "q_loops_1", "selected_answer": "10"},
            {"question_id": "q_arrays_1", "selected_answer": "O(1)"},
            {"question_id": "q_recursion_1", "selected_answer": "It automatically returns None after 10 calls"}  # Incorrect
        ]

        sub_res = await client.post("/api/assessment/submit", json={"answers": answers}, headers=headers)
        assert sub_res.status_code == 200
        result = sub_res.json()

        assert result["score"] == 0.67
        assert result["score_percentage"] == 67
        assert "loops" in result["strong_topics"]
        assert "arrays" in result["strong_topics"]
        assert "recursion" in result["weak_topics"]
        assert "gap_summary" in result
