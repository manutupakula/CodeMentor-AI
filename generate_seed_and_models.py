import os

BASE_DIR = r"C:\Users\Master_Manu\.gemini\antigravity\scratch\codementor-ai\backend"

def write_file(rel_path, content):
    full_path = os.path.join(BASE_DIR, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {rel_path}")

# app/models/user.py
write_file("app/models/user.py", """from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

class UserModel(BaseModel):
    id: str = Field(alias="_id")
    name: str
    email: EmailStr
    password_hash: str
    languages: List[str] = ["python"]
    self_declared_level: str = "intermediate"  # beginner, intermediate, advanced
    selected_topics: List[str] = []
    knowledge_check_completed: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
""")

# app/models/problem.py
write_file("app/models/problem.py", """from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ProblemTestCase(BaseModel):
    input_args: List[Any]
    expected_output: Any
    is_hidden: bool = False
    explanation: Optional[str] = None

class ProblemExample(BaseModel):
    input_str: str
    output_str: str
    explanation: Optional[str] = None

class ProblemModel(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: str
    topic: str               # Recursion, Loops, Arrays, Strings, Dictionaries, Searching, Sorting, OOP, DP, etc.
    subconcept: str          # base_case, loop_boundary, hash_lookup, two_pointer, etc.
    difficulty: str         # beginner, intermediate, advanced (or easy, medium, hard)
    language: str = "python"
    type: str = "coding"
    examples: List[Dict[str, Any]] = []
    constraints: List[str] = []
    starter_code: str
    test_cases: List[Dict[str, Any]] = []
    tags: List[str] = []
    estimated_time: int = 15  # in minutes
    
    # Secure server-side fields (Never exposed before unlock)
    solution: str
    explanation: str
    better_approach: str
    time_complexity: str
    space_complexity: str

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
""")

# app/models/assessment.py
write_file("app/models/assessment.py", """from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class QuestionAnswerRecord(BaseModel):
    question_id: str
    selected_answer: str
    correct: bool
    concept: str
    misconception: Optional[str] = None

class AssessmentModel(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    questions: List[Dict[str, Any]] = []
    score: float                      # 0.0 to 1.0
    concept_scores: Dict[str, float] = {}  # topic -> 0.0 to 1.0
    self_declared_level: str
    calculated_level: str
    comparison: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
""")

# app/models/session.py
write_file("app/models/session.py", """from datetime import datetime, timezone
from typing import Optional
from pydantic import BaseModel, Field

class SessionModel(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    problem_id: str
    topic: str
    attempts_allowed: int = 3
    attempts_used: int = 0
    hints_used: int = 0
    current_hint_level: int = 0      # 0, 1 (Socratic), 2 (Conceptual), 3 (Code Guidance)
    solution_unlocked: bool = False
    status: str = "in_progress"       # in_progress, solved_independently, solved_with_hints, exhausted, abandoned
    started_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
""")

# app/models/attempt.py
write_file("app/models/attempt.py", """from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class AttemptModel(BaseModel):
    id: str = Field(alias="_id")
    session_id: str
    user_id: str
    problem_id: str
    attempt_number: int
    code: str
    language: str = "python"
    execution_result: Dict[str, Any] = {}
    is_correct: bool = False
    error_type: str = "UNKNOWN"       # SYNTAX_ERROR, RUNTIME_ERROR, LOGICAL_ERROR, etc.
    concept: str = "general"
    subconcept: Optional[str] = None
    misconception: Optional[str] = None
    hint_level: int = 0
    hint_text: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
""")

# app/models/learner_profile.py
write_file("app/models/learner_profile.py", """from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class LearnerProfileModel(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    overall_level: str = "intermediate"
    self_assessment: str = "intermediate"
    knowledge_check_score: Optional[float] = None
    concept_mastery: Dict[str, float] = {}       # e.g., {"loops": 0.8, "recursion": 0.35}
    strong_topics: List[str] = []
    weak_topics: List[str] = []
    recurring_mistakes: Dict[str, int] = {}      # e.g., {"missing_base_case": 3, "off_by_one": 2}
    recent_performance: Dict[str, Any] = {
        "total_attempts": 0,
        "independent_solves": 0,
        "hint_assisted_solves": 0,
        "failed_sessions": 0
    }
    problems_solved: int = 0
    problems_attempted: int = 0
    hints_used: int = 0
    independent_solves: int = 0
    last_updated: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
""")

# app/models/conversation.py
write_file("app/models/conversation.py", """from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class ConversationMessage(BaseModel):
    role: str                       # student, tutor, system
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = {}

class ConversationModel(BaseModel):
    id: str = Field(alias="_id")
    session_id: str
    user_id: str
    problem_id: str
    messages: List[Dict[str, Any]] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True
    }
""")

print("Models created successfully.")
