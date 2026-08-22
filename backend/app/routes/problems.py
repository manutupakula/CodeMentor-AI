from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from app.schemas.problem import ProblemSummary, ProblemDetail
from app.routes.auth import get_current_user_dep
from app.db.mongodb import get_collection
from app.utils.errors import EntityNotFoundError

router = APIRouter(prefix="/api/problems", tags=["Problems"])

@router.get("", response_model=List[ProblemSummary])
async def list_problems(
    topic: Optional[str] = Query(None, description="Filter by topic"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    search: Optional[str] = Query(None, description="Search by title"),
    current_user: dict = Depends(get_current_user_dep)
):
    problems_col = get_collection("problems")
    query = {}
    if topic:
        query["topic"] = {"$regex": f"^{topic}$", "$options": "i"}
    if difficulty:
        query["difficulty"] = {"$regex": f"^{difficulty}$", "$options": "i"}
    if search:
        query["title"] = {"$regex": search, "$options": "i"}

    problems = await problems_col.find(query).to_list(200)
    summaries = []
    for p in problems:
        summaries.append({
            "id": str(p.get("_id") or p.get("id")),
            "title": p.get("title"),
            "topic": p.get("topic"),
            "subconcept": p.get("subconcept", "general"),
            "difficulty": p.get("difficulty"),
            "language": p.get("language", "python"),
            "estimated_time": p.get("estimated_time", 15),
            "tags": p.get("tags", [])
        })
    return summaries

@router.get("/{problem_id}", response_model=ProblemDetail)
async def get_problem(
    problem_id: str,
    current_user: dict = Depends(get_current_user_dep)
):
    problems_col = get_collection("problems")
    problem = await problems_col.find_one({"_id": problem_id}) or await problems_col.find_one({"id": problem_id})
    if not problem:
        raise EntityNotFoundError("Problem not found")

    # Securely omitting solution, explanation, better_approach
    return {
        "id": str(problem.get("_id") or problem.get("id")),
        "title": problem.get("title"),
        "description": problem.get("description"),
        "topic": problem.get("topic"),
        "subconcept": problem.get("subconcept", "general"),
        "difficulty": problem.get("difficulty"),
        "language": problem.get("language", "python"),
        "examples": problem.get("examples", []),
        "constraints": problem.get("constraints", []),
        "starter_code": problem.get("starter_code", ""),
        "tags": problem.get("tags", []),
        "estimated_time": problem.get("estimated_time", 15)
    }
