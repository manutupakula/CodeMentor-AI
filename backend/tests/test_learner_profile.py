import pytest
from app.services.learner_service import learner_service

def test_deterministic_mastery_calculation():
    # Scenario A: High assessment score, successful solves, independent solving
    mastery_a = learner_service.calculate_topic_mastery(
        assessment_score=0.90,
        topic_attempts=5,
        topic_solves=5,
        topic_independent_solves=4,
        recurring_mistake_count=0,
        hints_used=1
    )
    assert mastery_a >= 0.80

    # Scenario B: Low assessment score, multiple failed attempts, recurring mistakes
    mastery_b = learner_service.calculate_topic_mastery(
        assessment_score=0.20,
        topic_attempts=4,
        topic_solves=1,
        topic_independent_solves=0,
        recurring_mistake_count=3,
        hints_used=6
    )
    assert mastery_b <= 0.40
    assert mastery_a > mastery_b
