from typing import Optional, List
from pydantic import BaseModel, Field

class TutorAnalysis(BaseModel):
    correct: bool = Field(description="Whether the student code is fully correct and passes the problem requirements")
    error_type: str = Field(description="Standard error category: SYNTAX_ERROR, RUNTIME_ERROR, LOGICAL_ERROR, ALGORITHM_ERROR, EDGE_CASE_ERROR, COMPLEXITY_ERROR, CONCEPTUAL_MISUNDERSTANDING, STYLE_ISSUE, CORRECT, or UNKNOWN")
    concept: str = Field(description="The core programming concept involved, e.g. recursion, loops, arrays, base_case, binary_search")
    subconcept: Optional[str] = Field(default=None, description="More specific subconcept, e.g. loop_boundary, stopping_condition, mutable_default")
    misconception: Optional[str] = Field(default=None, description="The specific student misconception or reasoning mistake detected, e.g. missing_base_case, off_by_one, wrong_step")
    analysis: str = Field(description="Pedagogical diagnosis of the code, identifying what works and what is failing without giving away the direct code fix")
    hint: Optional[str] = Field(default=None, description="Progressive hint tailored strictly to current hint level. Level 1: Socratic question. Level 2: Conceptual explanation. Level 3: Concrete code guidance.")
    hint_level: int = Field(default=1, description="Current hint level (1, 2, or 3)")
    better_approach: Optional[str] = Field(default=None, description="More optimal approach or time/space optimization (only provided if solved or unlocked)")
    time_complexity: Optional[str] = Field(default=None, description="Big-O time complexity")
    space_complexity: Optional[str] = Field(default=None, description="Big-O space complexity")
    learning_tip: Optional[str] = Field(default=None, description="Actionable learning takeaway or reflection challenge for the student")

class ConversationReply(BaseModel):
    reply: str = Field(description="Pedagogical response to the student's question, adapting to their skill level")
    suggested_followups: List[str] = Field(default_factory=list, description="2-3 suggested follow-up questions the student might ask")
    concept: Optional[str] = Field(default=None, description="Primary concept discussed in this turn")

class KnowledgeGapExplanation(BaseModel):
    gap_summary: str = Field(description="Summary comparing self-declared skill level with actual knowledge check score")
    strong_topics_analysis: str = Field(description="Feedback on areas the student mastered")
    weak_topics_analysis: str = Field(description="Actionable feedback on areas needing practice")
    learning_path_recommendation: str = Field(description="Personalized next steps for learning")
