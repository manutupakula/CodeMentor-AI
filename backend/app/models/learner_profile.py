from datetime import datetime, timezone
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
