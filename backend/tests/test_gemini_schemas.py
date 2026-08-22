import pytest
from app.ai.schemas import TutorAnalysis, ConversationReply, KnowledgeGapExplanation

def test_tutor_analysis_schema_validation():
    valid_data = {
        "correct": False,
        "error_type": "LOGICAL_ERROR",
        "concept": "recursion",
        "subconcept": "base_case",
        "misconception": "missing_base_case",
        "analysis": "The recursive call does not reach a terminating condition.",
        "hint": "What value should the function return when n reaches 0?",
        "hint_level": 1,
        "better_approach": None,
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "learning_tip": "Always specify a base case."
    }
    analysis = TutorAnalysis.model_validate(valid_data)
    assert analysis.correct is False
    assert analysis.error_type == "LOGICAL_ERROR"
    assert analysis.hint_level == 1
    assert analysis.misconception == "missing_base_case"

def test_conversation_reply_schema():
    data = {
        "reply": "Think of the base case as the stopping point.",
        "suggested_followups": ["What if n is negative?", "Can we use iteration?"],
        "concept": "recursion"
    }
    reply = ConversationReply.model_validate(data)
    assert len(reply.suggested_followups) == 2
    assert reply.concept == "recursion"
