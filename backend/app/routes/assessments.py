from fastapi import APIRouter, Depends
from typing import Dict, Any, List
import uuid

from app.schemas.assessment import (
    AssessmentStartResponse,
    AssessmentSubmitRequest,
    AssessmentResultResponse,
    AssessmentQuestionItem
)
from app.routes.auth import get_current_user_dep
from app.services.assessment_service import assessment_service
from app.db.mongodb import get_collection
from app.utils.errors import EntityNotFoundError

router = APIRouter(prefix="/api/assessment", tags=["Knowledge Check Assessment"])

@router.post("/start", response_model=AssessmentStartResponse)
async def start_assessment(current_user: dict = Depends(get_current_user_dep)):
    questions = await assessment_service.get_questions_for_user(current_user)
    return {
        "assessment_id": str(uuid.uuid4()),
        "total_questions": len(questions),
        "questions": questions
    }

@router.post("/submit", response_model=AssessmentResultResponse)
async def submit_assessment(
    req: AssessmentSubmitRequest,
    current_user: dict = Depends(get_current_user_dep)
):
    answers_dict = [a.model_dump() for a in req.answers]
    result = await assessment_service.submit_assessment(current_user, answers_dict)
    return result

@router.get("/latest", response_model=AssessmentResultResponse)
async def get_latest_assessment(current_user: dict = Depends(get_current_user_dep)):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    assessments_col = get_collection("assessments")
    latest = await assessments_col.find({"user_id": user_id}).sort("created_at", -1).limit(1).to_list(1)
    if not latest:
        raise EntityNotFoundError("No completed knowledge check assessment found for this user.")
    
    doc = latest[0]
    comparison = doc.get("comparison", {})
    return {
        "id": str(doc.get("_id") or doc.get("id")),
        "score": doc.get("score", 0.0),
        "score_percentage": int(doc.get("score", 0.0) * 100),
        "self_declared_level": doc.get("self_declared_level", "intermediate"),
        "calculated_level": doc.get("calculated_level", "intermediate"),
        "strong_topics": comparison.get("strong_topics", []),
        "weak_topics": comparison.get("weak_topics", []),
        "concept_scores": doc.get("concept_scores", {}),
        "gap_summary": comparison.get("gap_summary", "Assessment completed."),
        "detailed_feedback": f"{comparison.get('strong_analysis', '')} {comparison.get('weak_analysis', '')} {comparison.get('learning_path', '')}"
    }
