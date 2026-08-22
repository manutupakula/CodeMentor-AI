from datetime import datetime, timezone
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
