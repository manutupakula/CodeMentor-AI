import logging
from typing import List, Dict, Any, Optional
from app.db.mongodb import get_collection
from app.services.learner_service import learner_service

logger = logging.getLogger("codementor.recommendation_service")

class RecommendationService:
    @classmethod
    async def get_personalized_recommendations(
        cls,
        user_id: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        profile = await learner_service.get_or_create_profile(user_id)
        problems_col = get_collection("problems")
        all_problems = await problems_col.find({}).to_list(100)
        
        # Get user sessions / solved problems
        sessions_col = get_collection("learning_sessions")
        user_sessions = await sessions_col.find({"user_id": user_id}).to_list(500)
        solved_problem_ids = {
            s["problem_id"] for s in user_sessions if s.get("status") in ["solved_independently", "solved_with_hints"]
        }
        attempted_problem_ids = {s["problem_id"] for s in user_sessions}

        concept_mastery = profile.get("concept_mastery", {})
        weak_topics = [t.lower() for t in profile.get("weak_topics", [])]
        recurring_mistakes = profile.get("recurring_mistakes", {})
        overall_level = profile.get("overall_level", "intermediate").lower()

        scored_problems = []

        for p in all_problems:
            pid = str(p.get("_id") or p.get("id"))
            ptopic = p.get("topic", "").lower()
            psubconcept = p.get("subconcept", "").lower()
            pdiff = p.get("difficulty", "intermediate").lower()

            # 1. Weakness Match (0.35)
            # Higher score if topic is in weak_topics or low mastery
            topic_mastery = concept_mastery.get(ptopic, 0.5)
            weakness_match = 1.0 - topic_mastery
            if ptopic in weak_topics:
                weakness_match = max(weakness_match, 0.85)

            # 2. Difficulty Match (0.25)
            if pdiff == overall_level or (overall_level == "beginner" and pdiff == "easy") or (overall_level == "intermediate" and pdiff == "medium"):
                difficulty_match = 1.0
            elif (overall_level == "beginner" and pdiff == "intermediate") or (overall_level == "intermediate" and pdiff == "hard"):
                difficulty_match = 0.5
            else:
                difficulty_match = 0.3

            # 3. Recent Failure Match / Misconception match (0.20)
            recent_failure_match = 0.0
            matching_mistakes = []
            for mistake, count in recurring_mistakes.items():
                if psubconcept in mistake or mistake in psubconcept or ptopic in mistake:
                    recent_failure_match = min(1.0, 0.4 + count * 0.2)
                    matching_mistakes.append((mistake, count))

            # 4. Topic Relevance (0.10)
            topic_relevance = 0.8 if ptopic in concept_mastery else 0.5

            # 5. Novelty (0.10)
            if pid not in attempted_problem_ids:
                novelty = 1.0
            elif pid not in solved_problem_ids:
                novelty = 0.6  # Needs retry
            else:
                novelty = 0.1  # Already solved

            total_score = (
                0.35 * weakness_match +
                0.25 * difficulty_match +
                0.20 * recent_failure_match +
                0.10 * topic_relevance +
                0.10 * novelty
            )

            # Generate natural explanation for recommendation
            if matching_mistakes:
                top_m, cnt = matching_mistakes[0]
                reason = f"Recommended because you struggled with {top_m.replace('_', ' ')} ({cnt} prior mistake{'s' if cnt > 1 else ''})."
            elif ptopic in weak_topics:
                reason = f"Recommended because {p.get('topic')} is currently marked as an area for improvement (mastery: {int(topic_mastery * 100)}%)."
            elif pid in attempted_problem_ids and pid not in solved_problem_ids:
                reason = f"Recommended to retry and master {p.get('topic')} ({psubconcept}) after previous attempts."
            elif pdiff == overall_level:
                reason = f"Recommended as an optimal {pdiff.capitalize()} challenge to reinforce your {p.get('topic')} problem solving."
            else:
                reason = f"Curated to broaden your problem-solving range in {p.get('topic')}."

            scored_problems.append({
                "problem_id": pid,
                "title": p.get("title"),
                "topic": p.get("topic"),
                "subconcept": p.get("subconcept"),
                "difficulty": p.get("difficulty"),
                "match_score": round(total_score, 2),
                "recommendation_reason": reason
            })

        # Sort descending by match score
        scored_problems.sort(key=lambda x: x["match_score"], reverse=True)
        return scored_problems[:limit]

    @classmethod
    async def get_mistake_revisions(cls, user_id: str) -> List[Dict[str, Any]]:
        profile = await learner_service.get_or_create_profile(user_id)
        recurring_mistakes = profile.get("recurring_mistakes", {})
        
        recs = await cls.get_personalized_recommendations(user_id, limit=10)
        recs_by_topic = {r["topic"].lower(): r for r in recs}

        revision_items = []
        advice_map = {
            "missing_base_case": ("Recursion", "Always specify one or more stopping conditions (base cases) before making any recursive call to prevent stack overflow."),
            "loop_boundary_or_indexing": ("Loops", "Check boundary offsets and remember that ranges in Python stop strictly at upper - 1."),
            "off_by_one": ("Arrays", "Double check your 0-based indexing calculations on first and last elements."),
            "syntax_formatting": ("Variables", "Pay close attention to colons, indentation levels, and closing brackets."),
            "recursion_logic_gap": ("Recursion", "Break the recursive problem into the smallest subproblem: solve the base case first, then step forward.")
        }

        for mistake, count in sorted(recurring_mistakes.items(), key=lambda x: x[1], reverse=True):
            concept, default_advice = advice_map.get(
                mistake,
                (mistake.split("_")[0].capitalize(), f"Focus on understanding the core invariant and edge cases for {mistake.replace('_', ' ')}.")
            )
            matched_prob = recs_by_topic.get(concept.lower())
            
            revision_items.append({
                "mistake_type": mistake.replace("_", " ").capitalize(),
                "count": count,
                "concept": concept,
                "advice": default_advice,
                "recommended_problem": matched_prob
            })

        return revision_items

recommendation_service = RecommendationService()
