import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import uuid

from app.db.mongodb import get_collection
from app.db.seed import KNOWLEDGE_CHECK_QUESTIONS
from app.services.learner_service import learner_service
from app.ai.gemini_client import gemini_client

logger = logging.getLogger("codementor.assessment_service")

class AssessmentService:
    @staticmethod
    async def get_questions_for_user(user: Dict[str, Any]) -> List[Dict[str, Any]]:
        assessments_bank = get_collection("assessment_bank")
        questions = await assessments_bank.find({}).to_list(100)
        if not questions:
            questions = KNOWLEDGE_CHECK_QUESTIONS
            
        # Return questions without correct answers and explanations for student security
        sanitized = []
        for q in questions:
            sanitized.append({
                "question_id": q.get("question_id"),
                "question": q.get("question"),
                "type": q.get("type", "mcq"),
                "topic": q.get("topic", "General"),
                "subconcept": q.get("subconcept", "general"),
                "difficulty": q.get("difficulty", "beginner"),
                "options": q.get("options", [])
            })
        return sanitized

    @classmethod
    async def submit_assessment(
        cls,
        user: Dict[str, Any],
        answers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        assessments_bank = get_collection("assessment_bank")
        all_questions = await assessments_bank.find({}).to_list(100)
        if not all_questions:
            all_questions = KNOWLEDGE_CHECK_QUESTIONS
            
        q_map = {q["question_id"]: q for q in all_questions}
        
        user_id = str(user.get("_id") or user.get("id"))
        self_level = user.get("self_declared_level", "intermediate")
        languages = user.get("languages", ["python"])

        # Deterministic Scoring
        total_questions = len(answers)
        correct_count = 0
        topic_totals: Dict[str, int] = {}
        topic_correct: Dict[str, int] = {}
        detailed_records = []

        for item in answers:
            qid = item.get("question_id")
            selected = str(item.get("selected_answer", "")).strip()
            q_info = q_map.get(qid)
            
            if not q_info:
                continue

            topic = q_info.get("topic", "General")
            correct_ans = str(q_info.get("correct_answer", "")).strip()
            is_correct = (selected.lower() == correct_ans.lower())
            
            topic_totals[topic] = topic_totals.get(topic, 0) + 1
            if is_correct:
                correct_count += 1
                topic_correct[topic] = topic_correct.get(topic, 0) + 1
            
            detailed_records.append({
                "question_id": qid,
                "selected_answer": selected,
                "correct": is_correct,
                "concept": topic.lower(),
                "misconception": q_info.get("misconception") if not is_correct else None
            })

        overall_score = round(correct_count / max(1, total_questions), 2)
        score_pct = int(overall_score * 100)

        # Concept Breakdown
        concept_scores = {}
        strong_topics = []
        weak_topics = []

        for topic, tot in topic_totals.items():
            corr = topic_correct.get(topic, 0)
            t_score = round(corr / tot, 2)
            concept_scores[topic.lower()] = t_score
            if t_score >= 0.70:
                strong_topics.append(topic.lower())
            elif t_score < 0.60:
                weak_topics.append(topic.lower())

        # Determine calculated level deterministically
        if overall_score >= 0.80:
            calculated_level = "advanced"
        elif overall_score >= 0.50:
            calculated_level = "intermediate"
        else:
            calculated_level = "beginner"

        # Generate natural language gap analysis via Gemini / AI layer
        gap_exp = await gemini_client.explain_assessment_gap(
            self_level=self_level,
            languages=languages,
            score_percentage=score_pct,
            correct_count=correct_count,
            total_count=total_questions,
            calculated_level=calculated_level,
            topic_scores=concept_scores,
            strong_topics=strong_topics,
            weak_topics=weak_topics
        )

        assessment_doc = {
            "_id": str(uuid.uuid4()),
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "questions": detailed_records,
            "score": overall_score,
            "concept_scores": concept_scores,
            "self_declared_level": self_level,
            "calculated_level": calculated_level,
            "comparison": {
                "strong_topics": strong_topics,
                "weak_topics": weak_topics,
                "gap_summary": gap_exp.gap_summary,
                "strong_analysis": gap_exp.strong_topics_analysis,
                "weak_analysis": gap_exp.weak_topics_analysis,
                "learning_path": gap_exp.learning_path_recommendation
            },
            "created_at": datetime.now(timezone.utc)
        }

        # Store assessment
        assessments_col = get_collection("assessments")
        await assessments_col.insert_one(assessment_doc)

        # Update User status
        users_col = get_collection("users")
        await users_col.update_one(
            {"_id": user_id},
            {"$set": {"knowledge_check_completed": True, "updated_at": datetime.now(timezone.utc)}}
        )

        # Update Learner Profile
        await learner_service.update_profile_from_assessment(
            user_id=user_id,
            assessment_score=overall_score,
            calculated_level=calculated_level,
            concept_scores=concept_scores,
            strong_topics=strong_topics,
            weak_topics=weak_topics
        )

        return {
            "id": assessment_doc["_id"],
            "score": overall_score,
            "score_percentage": score_pct,
            "self_declared_level": self_level,
            "calculated_level": calculated_level,
            "strong_topics": strong_topics,
            "weak_topics": weak_topics,
            "concept_scores": concept_scores,
            "gap_summary": gap_exp.gap_summary,
            "detailed_feedback": f"{gap_exp.strong_topics_analysis} {gap_exp.weak_topics_analysis} {gap_exp.learning_path_recommendation}"
        }

assessment_service = AssessmentService()
