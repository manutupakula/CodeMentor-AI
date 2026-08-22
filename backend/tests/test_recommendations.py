import pytest
import pytest_asyncio
from app.db.mongodb import init_db, close_db, get_database, get_collection
from app.db.seed import seed_database
from app.services.recommendation_service import recommendation_service

@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    await init_db()
    db = get_database()
    await seed_database(db)
    yield
    await close_db()

@pytest.mark.asyncio
async def test_problem_recommendations_and_weak_topic_matching():
    user_id = "test_user_rec_1"
    profiles_col = get_collection("learner_profiles")
    
    # Create profile with weak recursion and recurring base case mistakes
    await profiles_col.insert_one({
        "_id": user_id,
        "user_id": user_id,
        "overall_level": "intermediate",
        "concept_mastery": {"recursion": 0.25, "arrays": 0.85, "loops": 0.80},
        "strong_topics": ["arrays", "loops"],
        "weak_topics": ["recursion"],
        "recurring_mistakes": {"missing_base_case": 3},
        "recent_performance": {"total_attempts": 5, "independent_solves": 2, "hint_assisted_solves": 1, "failed_sessions": 2},
        "problems_solved": 3,
        "problems_attempted": 5,
        "hints_used": 6,
        "independent_solves": 2
    })

    recs = await recommendation_service.get_personalized_recommendations(user_id=user_id, limit=3)
    assert len(recs) > 0
    # Top recommendation should prioritize the weak topic (Recursion)
    top_rec = recs[0]
    assert top_rec["topic"] == "Recursion"
    assert "recursion" in top_rec["recommendation_reason"].lower() or "base case" in top_rec["recommendation_reason"].lower()
