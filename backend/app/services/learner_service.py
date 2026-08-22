import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import uuid
from app.db.mongodb import get_collection
from app.models.learner_profile import LearnerProfileModel

logger = logging.getLogger("codementor.learner_service")

class LearnerProfileService:
    @staticmethod
    async def get_or_create_profile(user_id: str, self_level: str = "intermediate") -> Dict[str, Any]:
        profiles_col = get_collection("learner_profiles")
        profile = await profiles_col.find_one({"user_id": user_id})
        if not profile:
            new_profile = {
                "_id": str(uuid.uuid4()),
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "overall_level": self_level,
                "self_assessment": self_level,
                "knowledge_check_score": None,
                "concept_mastery": {
                    "variables": 0.5,
                    "conditions": 0.5,
                    "loops": 0.5,
                    "functions": 0.5,
                    "arrays": 0.5,
                    "strings": 0.5,
                    "dictionaries": 0.5,
                    "searching": 0.5,
                    "sorting": 0.5,
                    "recursion": 0.5,
                    "oop": 0.5,
                    "dynamic_programming": 0.5
                },
                "strong_topics": [],
                "weak_topics": [],
                "recurring_mistakes": {},
                "recent_performance": {
                    "total_attempts": 0,
                    "independent_solves": 0,
                    "hint_assisted_solves": 0,
                    "failed_sessions": 0
                },
                "problems_solved": 0,
                "problems_attempted": 0,
                "hints_used": 0,
                "independent_solves": 0,
                "last_updated": datetime.now(timezone.utc)
            }
            await profiles_col.insert_one(new_profile)
            return new_profile
        return profile

    @staticmethod
    def calculate_topic_mastery(
        assessment_score: Optional[float],
        topic_attempts: int,
        topic_solves: int,
        topic_independent_solves: int,
        recurring_mistake_count: int,
        hints_used: int
    ) -> float:
        """
        Deterministic formula:
        mastery = 0.40 * assessment_score + 0.30 * problem_success + 0.20 * independent_solving + 0.10 * recent_performance - penalties
        """
        # Baseline from assessment
        base_assessment = assessment_score if assessment_score is not None else 0.50
        
        # Problem success rate
        problem_success = (topic_solves / topic_attempts) if topic_attempts > 0 else base_assessment
        
        # Independent solving rate
        ind_rate = (topic_independent_solves / topic_solves) if topic_solves > 0 else 0.0
        
        # Recent performance
        recent_perf = min(1.0, topic_solves * 0.25)
        
        raw_mastery = (
            0.40 * base_assessment +
            0.30 * problem_success +
            0.20 * ind_rate +
            0.10 * recent_perf
        )
        
        # Apply penalties for recurring mistakes and heavy hint reliance
        mistake_penalty = min(0.20, recurring_mistake_count * 0.05)
        hint_penalty = min(0.15, (hints_used / max(1, topic_attempts)) * 0.05)
        
        final_mastery = max(0.05, min(0.99, raw_mastery - mistake_penalty - hint_penalty))
        return round(final_mastery, 2)

    @classmethod
    async def update_profile_from_assessment(
        cls,
        user_id: str,
        assessment_score: float,
        calculated_level: str,
        concept_scores: Dict[str, float],
        strong_topics: List[str],
        weak_topics: List[str]
    ):
        profiles_col = get_collection("learner_profiles")
        profile = await cls.get_or_create_profile(user_id)
        
        mastery = profile.get("concept_mastery", {})
        for topic, score in concept_scores.items():
            topic_key = topic.lower()
            mastery[topic_key] = round(score, 2)
            
        await profiles_col.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "overall_level": calculated_level,
                    "knowledge_check_score": assessment_score,
                    "concept_mastery": mastery,
                    "strong_topics": [t.lower() for t in strong_topics],
                    "weak_topics": [t.lower() for t in weak_topics],
                    "last_updated": datetime.now(timezone.utc)
                }
            }
        )

    @classmethod
    async def update_profile_after_attempt(
        cls,
        user_id: str,
        topic: str,
        is_correct: bool,
        error_type: str,
        misconception: Optional[str],
        hint_level: int,
        is_session_solved: bool,
        is_independent: bool
    ):
        profiles_col = get_collection("learner_profiles")
        profile = await cls.get_or_create_profile(user_id)
        
        topic_key = topic.lower()
        mastery_dict = profile.get("concept_mastery", {})
        current_topic_mastery = mastery_dict.get(topic_key, 0.5)
        
        mistakes = profile.get("recurring_mistakes", {})
        if misconception:
            mistakes[misconception] = mistakes.get(misconception, 0) + 1

        perf = profile.get("recent_performance", {})
        perf["total_attempts"] = perf.get("total_attempts", 0) + 1
        
        problems_solved = profile.get("problems_solved", 0)
        independent_solves = profile.get("independent_solves", 0)
        hints_used = profile.get("hints_used", 0) + (1 if hint_level > 0 else 0)

        if is_session_solved:
            problems_solved += 1
            if is_independent:
                independent_solves += 1
                perf["independent_solves"] = perf.get("independent_solves", 0) + 1
                # Boost mastery
                current_topic_mastery = min(0.99, current_topic_mastery + 0.10)
            else:
                perf["hint_assisted_solves"] = perf.get("hint_assisted_solves", 0) + 1
                current_topic_mastery = min(0.95, current_topic_mastery + 0.05)
        else:
            if not is_correct:
                # Lower mastery slightly on mistake
                current_topic_mastery = max(0.10, current_topic_mastery - 0.04)

        mastery_dict[topic_key] = round(current_topic_mastery, 2)

        # Re-evaluate strong and weak topics
        strong_topics = [t for t, score in mastery_dict.items() if score >= 0.70]
        weak_topics = [t for t, score in mastery_dict.items() if score < 0.60]

        await profiles_col.update_one(
            {"user_id": user_id},
            {
                "$set": {
                    "concept_mastery": mastery_dict,
                    "strong_topics": strong_topics,
                    "weak_topics": weak_topics,
                    "recurring_mistakes": mistakes,
                    "recent_performance": perf,
                    "problems_solved": problems_solved,
                    "independent_solves": independent_solves,
                    "hints_used": hints_used,
                    "last_updated": datetime.now(timezone.utc)
                }
            }
        )

learner_service = LearnerProfileService()
