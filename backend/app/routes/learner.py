from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
from app.schemas.learner import (
    LearnerProfileResponse,
    ProblemRecommendationItem,
    MistakeRevisionItem
)
from app.routes.auth import get_current_user_dep
from app.services.learner_service import learner_service
from app.services.recommendation_service import recommendation_service
from app.db.mongodb import get_collection

router = APIRouter(prefix="/api/learner", tags=["Learner Profile & Recommendations"])

@router.get("/profile", response_model=LearnerProfileResponse)
async def get_learner_profile(current_user: dict = Depends(get_current_user_dep)):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    profile = await learner_service.get_or_create_profile(user_id, current_user.get("self_declared_level", "intermediate"))
    return profile

@router.get("/weak-topics", response_model=List[str])
async def get_weak_topics(current_user: dict = Depends(get_current_user_dep)):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    profile = await learner_service.get_or_create_profile(user_id)
    return profile.get("weak_topics", [])

@router.get("/recommendations", response_model=List[ProblemRecommendationItem])
async def get_recommendations(
    limit: int = Query(5, ge=1, le=20),
    current_user: dict = Depends(get_current_user_dep)
):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    return await recommendation_service.get_personalized_recommendations(user_id=user_id, limit=limit)

@router.get("/revise-mistakes", response_model=List[MistakeRevisionItem])
async def get_revise_mistakes(current_user: dict = Depends(get_current_user_dep)):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    return await recommendation_service.get_mistake_revisions(user_id=user_id)

@router.get("/history", response_model=List[Dict[str, Any]])
async def get_learning_history(
    limit: int = Query(20, ge=1, le=100),
    current_user: dict = Depends(get_current_user_dep)
):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    sessions_col = get_collection("learning_sessions")
    sessions = await sessions_col.find({"user_id": user_id}).sort("started_at", -1).limit(limit).to_list(limit)
    
    problems_col = get_collection("problems")
    history = []
    for s in sessions:
        p = await problems_col.find_one({"_id": s["problem_id"]}) or await problems_col.find_one({"id": s["problem_id"]})
        history.append({
            "session_id": str(s.get("_id") or s.get("id")),
            "problem_id": s["problem_id"],
            "problem_title": p.get("title", "Problem") if p else "Problem",
            "topic": s.get("topic", "General"),
            "status": s.get("status", "in_progress"),
            "attempts_used": s.get("attempts_used", 0),
            "hints_used": s.get("hints_used", 0),
            "solution_unlocked": s.get("solution_unlocked", False),
            "started_at": s["started_at"],
            "completed_at": s.get("completed_at")
        })
    return history
