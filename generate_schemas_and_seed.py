import os

BASE_DIR = r"C:\Users\Master_Manu\.gemini\antigravity\scratch\codementor-ai\backend"

def write_file(rel_path, content):
    full_path = os.path.join(BASE_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {rel_path}")

# app/schemas/auth.py
write_file("app/schemas/auth.py", """from typing import List, Optional
from pydantic import BaseModel, EmailStr

class UserRegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    languages: List[str] = ["python"]
    self_declared_level: str = "intermediate"  # beginner, intermediate, advanced
    selected_topics: List[str] = []

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    languages: Optional[List[str]] = None
    self_declared_level: Optional[str] = None
    selected_topics: Optional[List[str]] = None

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    languages: List[str]
    self_declared_level: str
    selected_topics: List[str]
    knowledge_check_completed: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
""")

# app/schemas/problem.py
write_file("app/schemas/problem.py", """from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ProblemSummary(BaseModel):
    id: str
    title: str
    topic: str
    subconcept: str
    difficulty: str
    language: str
    estimated_time: int
    tags: List[str]

class ProblemDetail(BaseModel):
    id: str
    title: str
    description: str
    topic: str
    subconcept: str
    difficulty: str
    language: str
    examples: List[Dict[str, Any]]
    constraints: List[str]
    starter_code: str
    tags: List[str]
    estimated_time: int
    # Note: solution, explanation, better_approach, complexity are strictly omitted here

class ProblemSolutionResponse(BaseModel):
    problem_id: str
    solution: str
    explanation: str
    better_approach: str
    time_complexity: str
    space_complexity: str
    unlocked_reason: str
""")

# app/schemas/assessment.py
write_file("app/schemas/assessment.py", """from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class AssessmentQuestionItem(BaseModel):
    question_id: str
    question: str
    type: str               # mcq, predict_output, identify_bug, complexity
    topic: str
    subconcept: str
    difficulty: str
    options: List[str]
    # correct_answer & explanation omitted when serving question to student!

class AssessmentStartResponse(BaseModel):
    assessment_id: str
    total_questions: int
    questions: List[AssessmentQuestionItem]

class QuestionAnswerSubmission(BaseModel):
    question_id: str
    selected_answer: str

class AssessmentSubmitRequest(BaseModel):
    assessment_id: Optional[str] = None
    answers: List[QuestionAnswerSubmission]

class TopicPerformance(BaseModel):
    topic: str
    score: float
    status: str             # strong, moderate, weak

class AssessmentResultResponse(BaseModel):
    id: str
    score: float
    score_percentage: int
    self_declared_level: str
    calculated_level: str
    strong_topics: List[str]
    weak_topics: List[str]
    concept_scores: Dict[str, float]
    gap_summary: str
    detailed_feedback: str
""")

# app/schemas/session.py
write_file("app/schemas/session.py", """from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class SessionCreateRequest(BaseModel):
    problem_id: str

class SessionResponse(BaseModel):
    id: str
    user_id: str
    problem_id: str
    topic: str
    attempts_allowed: int
    attempts_used: int
    attempts_remaining: int
    hints_used: int
    current_hint_level: int
    solution_unlocked: bool
    status: str
    started_at: datetime
    completed_at: Optional[datetime] = None
""")

# app/schemas/tutor.py
write_file("app/schemas/tutor.py", """from typing import Optional, Dict, Any, List
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
""")

# app/schemas/learner.py
write_file("app/schemas/learner.py", """from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ProblemRecommendationItem(BaseModel):
    problem_id: str
    title: str
    topic: str
    subconcept: str
    difficulty: str
    match_score: float
    recommendation_reason: str

class LearnerProfileResponse(BaseModel):
    user_id: str
    overall_level: str
    self_assessment: str
    knowledge_check_score: Optional[float]
    concept_mastery: Dict[str, float]
    strong_topics: List[str]
    weak_topics: List[str]
    recurring_mistakes: Dict[str, int]
    recent_performance: Dict[str, Any]
    problems_solved: int
    problems_attempted: int
    hints_used: int
    independent_solves: int
    last_updated: datetime

class MistakeRevisionItem(BaseModel):
    mistake_type: str
    count: int
    concept: str
    advice: str
    recommended_problem: Optional[ProblemRecommendationItem] = None
""")

print("Schemas created successfully.")
