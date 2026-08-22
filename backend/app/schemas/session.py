from datetime import datetime
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
