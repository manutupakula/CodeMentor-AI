from datetime import datetime, timezone
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
