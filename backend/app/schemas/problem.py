from typing import List, Dict, Any, Optional
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
