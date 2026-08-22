from fastapi import APIRouter, Depends, status
from app.schemas.session import SessionCreateRequest, SessionResponse
from app.schemas.tutor import AttemptSubmitRequest, AttemptResponse, HintRequest, HintResponse
from app.schemas.problem import ProblemSolutionResponse
from app.routes.auth import get_current_user_dep
from app.services.tutor_service import tutor_service
from app.db.mongodb import get_collection
from app.utils.errors import EntityNotFoundError, ForbiddenAccessError

router = APIRouter(prefix="/api/sessions", tags=["Learning Sessions"])

@router.post("", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    req: SessionCreateRequest,
    current_user: dict = Depends(get_current_user_dep)
):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    session = await tutor_service.create_session(user_id=user_id, problem_id=req.problem_id)
    return {
        "id": session["id"],
        "user_id": session["user_id"],
        "problem_id": session["problem_id"],
        "topic": session.get("topic", "General"),
        "attempts_allowed": session.get("attempts_allowed", 3),
        "attempts_used": session.get("attempts_used", 0),
        "attempts_remaining": session.get("attempts_allowed", 3) - session.get("attempts_used", 0),
        "hints_used": session.get("hints_used", 0),
        "current_hint_level": session.get("current_hint_level", 0),
        "solution_unlocked": session.get("solution_unlocked", False),
        "status": session.get("status", "in_progress"),
        "started_at": session["started_at"],
        "completed_at": session.get("completed_at")
    }

@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    current_user: dict = Depends(get_current_user_dep)
):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    sessions_col = get_collection("learning_sessions")
    session = await sessions_col.find_one({"_id": session_id}) or await sessions_col.find_one({"id": session_id})
    if not session:
        raise EntityNotFoundError("Session not found")
    if session["user_id"] != user_id:
        raise ForbiddenAccessError("Unauthorized access to this session")

    return {
        "id": str(session.get("_id") or session.get("id")),
        "user_id": session["user_id"],
        "problem_id": session["problem_id"],
        "topic": session.get("topic", "General"),
        "attempts_allowed": session.get("attempts_allowed", 3),
        "attempts_used": session.get("attempts_used", 0),
        "attempts_remaining": max(0, session.get("attempts_allowed", 3) - session.get("attempts_used", 0)),
        "hints_used": session.get("hints_used", 0),
        "current_hint_level": session.get("current_hint_level", 0),
        "solution_unlocked": session.get("solution_unlocked", False),
        "status": session.get("status", "in_progress"),
        "started_at": session["started_at"],
        "completed_at": session.get("completed_at")
    }

@router.post("/{session_id}/attempt", response_model=AttemptResponse)
async def submit_attempt(
    session_id: str,
    req: AttemptSubmitRequest,
    current_user: dict = Depends(get_current_user_dep)
):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    result = await tutor_service.submit_attempt(
        user_id=user_id,
        session_id=session_id,
        code=req.code,
        language=req.language
    )
    return result

@router.post("/{session_id}/hint", response_model=HintResponse)
async def request_hint(
    session_id: str,
    req: HintRequest = HintRequest(),
    current_user: dict = Depends(get_current_user_dep)
):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    return await tutor_service.request_hint(
        user_id=user_id,
        session_id=session_id,
        requested_level=req.requested_level
    )

@router.get("/{session_id}/solution", response_model=ProblemSolutionResponse)
async def get_solution(
    session_id: str,
    current_user: dict = Depends(get_current_user_dep)
):
    user_id = str(current_user.get("_id") or current_user.get("id"))
    return await tutor_service.get_solution(user_id=user_id, session_id=session_id)
