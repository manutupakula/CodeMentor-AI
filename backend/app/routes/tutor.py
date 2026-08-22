from fastapi import APIRouter, Depends
from app.schemas.tutor import (
    TutorChatRequest,
    TutorChatResponse,
    CustomProblemAnalysisRequest,
    CustomProblemAnalysisResponse
)
from app.routes.auth import get_current_user_dep
from app.services.tutor_service import tutor_service

router = APIRouter(prefix="/api/tutor", tags=["AI Tutor Interaction"])

@router.post("/chat", response_model=TutorChatResponse)
async def chat_with_tutor(
    req: TutorChatRequest,
    current_user: dict = Depends(get_current_user_dep)
):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    return await tutor_service.chat_with_tutor(
        user_id=user_id,
        session_id=req.session_id,
        problem_id=req.problem_id,
        code=req.code,
        message=req.message
    )

@router.post("/custom-problem", response_model=CustomProblemAnalysisResponse)
async def analyze_custom_problem(
    req: CustomProblemAnalysisRequest,
    current_user: dict = Depends(get_current_user_dep)
):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    return await tutor_service.analyze_custom_problem(
        user_id=user_id,
        problem_title=req.problem_title,
        problem_description=req.problem_description,
        student_code=req.student_code,
        language=req.language,
        hint_level=req.hint_level
    )
