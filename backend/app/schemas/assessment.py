from typing import List, Dict, Any, Optional
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
