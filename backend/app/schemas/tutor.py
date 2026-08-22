from typing import Optional, Dict, Any, List
from pydantic import BaseModel

class AttemptSubmitRequest(BaseModel):
    code: str
    language: str = "python"

class AttemptResponse(BaseModel):
    attempt_id: str
    session_id: str
    is_correct: bool
    attempt_number: int
    attempts_remaining: int
    error_type: str
    concept: str
    subconcept: Optional[str] = None
    misconception: Optional[str] = None
    analysis: str
    hint: Optional[str] = None
    hint_level: int
    solution_unlocked: bool
    execution_result: Optional[Dict[str, Any]] = None
    # Unlocked fields (only if solution_unlocked is true)
    solution: Optional[str] = None
    explanation: Optional[str] = None
    better_approach: Optional[str] = None
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None
    learning_tip: Optional[str] = None

class HintRequest(BaseModel):
    requested_level: Optional[int] = None

class HintResponse(BaseModel):
    hint_level: int
    hint_title: str
    hint_text: str
    hints_remaining: int
    solution_unlocked: bool

class TutorChatRequest(BaseModel):
    session_id: Optional[str] = None
    problem_id: Optional[str] = None
    code: Optional[str] = None
    message: str

class TutorChatResponse(BaseModel):
    reply: str
    suggested_followups: List[str] = []
    concept: Optional[str] = None

class CustomProblemAnalysisRequest(BaseModel):
    problem_title: str
    problem_description: str
    student_code: str
    language: str = "python"
    hint_level: int = 1

class CustomProblemAnalysisResponse(BaseModel):
    is_correct: bool
    error_type: str
    concept: str
    misconception: Optional[str] = None
    analysis: str
    hint: str
    hint_level: int
    learning_tip: Optional[str] = None
