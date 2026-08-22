from datetime import datetime
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
