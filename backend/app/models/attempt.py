from datetime import datetime, timezone
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
