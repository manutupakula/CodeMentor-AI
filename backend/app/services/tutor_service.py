import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import uuid

from app.db.mongodb import get_collection
from app.execution.code_runner import SafeCodeRunner
from app.ai.gemini_client import gemini_client
from app.ai.context_builder import StudentContextBuilder
from app.services.learner_service import learner_service
from app.utils.errors import (
    EntityNotFoundError,
    ForbiddenAccessError,
    SolutionLockedError,
    AttemptsExhaustedError
)

logger = logging.getLogger("codementor.tutor_service")

class TutorOrchestratorService:
    @staticmethod
    async def create_session(user_id: str, problem_id: str) -> Dict[str, Any]:
        problems_col = get_collection("problems")
        problem = await problems_col.find_one({"_id": problem_id})
        if not problem:
            problem = await problems_col.find_one({"id": problem_id})
        if not problem:
            raise EntityNotFoundError("Problem not found")

        session_id = str(uuid.uuid4())
        session_doc = {
            "_id": session_id,
            "id": session_id,
            "user_id": user_id,
            "problem_id": problem_id,
            "topic": problem.get("topic", "General"),
            "attempts_allowed": 3,
            "attempts_used": 0,
            "hints_used": 0,
            "current_hint_level": 0,
            "solution_unlocked": False,
            "status": "in_progress",
            "started_at": datetime.now(timezone.utc),
            "completed_at": None
        }

        sessions_col = get_collection("learning_sessions")
        await sessions_col.insert_one(session_doc)
        return session_doc

    @classmethod
    async def submit_attempt(
        cls,
        user_id: str,
        session_id: str,
        code: str,
        language: str = "python"
    ) -> Dict[str, Any]:
        sessions_col = get_collection("learning_sessions")
        session = await sessions_col.find_one({"_id": session_id})
        if not session:
            session = await sessions_col.find_one({"id": session_id})
        if not session:
            raise EntityNotFoundError("Learning session not found")

        if session["user_id"] != user_id:
            raise ForbiddenAccessError("You are not authorized to submit to this session.")

        if session.get("attempts_used", 0) >= session.get("attempts_allowed", 3) and not session.get("solution_unlocked"):
            raise AttemptsExhaustedError("All allowed attempts for this session have been exhausted.")

        problems_col = get_collection("problems")
        problem = await problems_col.find_one({"_id": session["problem_id"]})
        if not problem:
            problem = await problems_col.find_one({"id": session["problem_id"]})
        if not problem:
            raise EntityNotFoundError("Associated problem not found")

        # 1. Execute Code
        test_cases = problem.get("test_cases", [])
        exec_result = await SafeCodeRunner.run_code(code=code, test_cases=test_cases)
        is_correct = exec_result.success

        # 2. Advance Session State
        attempts_used = session.get("attempts_used", 0) + 1
        attempts_allowed = session.get("attempts_allowed", 3)
        attempts_remaining = max(0, attempts_allowed - attempts_used)
        
        hint_level = min(3, max(1, attempts_used))
        hints_used = max(session.get("hints_used", 0), hint_level)

        solution_unlocked = session.get("solution_unlocked", False)
        status = session.get("status", "in_progress")

        if is_correct:
            solution_unlocked = True
            is_independent = (hints_used == 0 or attempts_used == 1)
            status = "solved_independently" if is_independent else "solved_with_hints"
            completed_at = datetime.now(timezone.utc)
        elif attempts_used >= attempts_allowed:
            solution_unlocked = True
            status = "exhausted"
            completed_at = datetime.now(timezone.utc)
        else:
            completed_at = None

        # 3. Build Student Context for AI
        users_col = get_collection("users")
        user = await users_col.find_one({"_id": user_id}) or {}
        learner_profile = await learner_service.get_or_create_profile(user_id)
        student_context = StudentContextBuilder.build_compact_context(user, learner_profile)

        # 4. Call Gemini AI Tutor
        tutor_analysis = await gemini_client.analyze_code(
            student_context=student_context,
            problem=problem,
            student_code=code,
            execution_result=exec_result.to_dict(),
            attempt_number=attempts_used,
            attempts_allowed=attempts_allowed,
            hint_level=hint_level,
            solution_unlocked=solution_unlocked
        )

        # 5. Record Attempt
        attempt_id = str(uuid.uuid4())
        attempt_doc = {
            "_id": attempt_id,
            "id": attempt_id,
            "session_id": session_id,
            "user_id": user_id,
            "problem_id": session["problem_id"],
            "attempt_number": attempts_used,
            "code": code,
            "language": language,
            "execution_result": exec_result.to_dict(),
            "is_correct": is_correct,
            "error_type": tutor_analysis.error_type,
            "concept": tutor_analysis.concept,
            "subconcept": tutor_analysis.subconcept,
            "misconception": tutor_analysis.misconception,
            "hint_level": hint_level,
            "hint_text": tutor_analysis.hint,
            "created_at": datetime.now(timezone.utc)
        }
        attempts_col = get_collection("attempts")
        await attempts_col.insert_one(attempt_doc)

        # 6. Update Learner Profile
        await learner_service.update_profile_after_attempt(
            user_id=user_id,
            topic=problem.get("topic", "General"),
            is_correct=is_correct,
            error_type=tutor_analysis.error_type,
            misconception=tutor_analysis.misconception,
            hint_level=hint_level,
            is_session_solved=is_correct,
            is_independent=(is_correct and attempts_used == 1 and hints_used <= 1)
        )

        # 7. Update Session
        await sessions_col.update_one(
            {"_id": session_id},
            {
                "$set": {
                    "attempts_used": attempts_used,
                    "hints_used": hints_used,
                    "current_hint_level": hint_level,
                    "solution_unlocked": solution_unlocked,
                    "status": status,
                    "completed_at": completed_at
                }
            }
        )

        # 8. Construct Response (Strictly enforce solution omission if locked)
        return {
            "attempt_id": attempt_id,
            "session_id": session_id,
            "is_correct": is_correct,
            "attempt_number": attempts_used,
            "attempts_remaining": attempts_remaining,
            "error_type": tutor_analysis.error_type,
            "concept": tutor_analysis.concept,
            "subconcept": tutor_analysis.subconcept,
            "misconception": tutor_analysis.misconception,
            "analysis": tutor_analysis.analysis,
            "hint": tutor_analysis.hint,
            "hint_level": hint_level,
            "solution_unlocked": solution_unlocked,
            "execution_result": exec_result.to_dict(),
            "solution": problem.get("solution") if solution_unlocked else None,
            "explanation": tutor_analysis.analysis if solution_unlocked else None,
            "better_approach": (tutor_analysis.better_approach or problem.get("better_approach")) if solution_unlocked else None,
            "time_complexity": (tutor_analysis.time_complexity or problem.get("time_complexity")) if solution_unlocked else None,
            "space_complexity": (tutor_analysis.space_complexity or problem.get("space_complexity")) if solution_unlocked else None,
            "learning_tip": tutor_analysis.learning_tip
        }

    @classmethod
    async def request_hint(
        cls,
        user_id: str,
        session_id: str,
        requested_level: Optional[int] = None
    ) -> Dict[str, Any]:
        sessions_col = get_collection("learning_sessions")
        session = await sessions_col.find_one({"_id": session_id})
        if not session:
            session = await sessions_col.find_one({"id": session_id})
        if not session:
            raise EntityNotFoundError("Session not found")

        if session["user_id"] != user_id:
            raise ForbiddenAccessError("Unauthorized access to session")

        current_level = session.get("current_hint_level", 0)
        target_level = requested_level if requested_level else min(3, current_level + 1)
        target_level = max(1, min(3, target_level))

        problems_col = get_collection("problems")
        problem = await problems_col.find_one({"_id": session["problem_id"]})
        if not problem:
            problem = await problems_col.find_one({"id": session["problem_id"]})

        topic = problem.get("topic", "General") if problem else "General"
        subconcept = problem.get("subconcept", "logic") if problem else "logic"

        hint_titles = {
            1: "Hint Level 1 (Socratic Discovery)",
            2: "Hint Level 2 (Conceptual Mechanism)",
            3: "Hint Level 3 (Code Directional Guidance)"
        }

        # Generate or pick progressive hint
        if target_level == 1:
            hint_text = f"What happens during the initial state and boundary condition in {topic.lower()} ({subconcept})? Trace a simple 1-element input."
        elif target_level == 2:
            hint_text = f"In {topic}, ensure that each step properly transitions state without skipping boundary elements or causing runaway recursion."
        else:
            hint_text = f"Review the specific condition guards and index references in your solution for {problem.get('title', 'this problem')}."

        hints_used = max(session.get("hints_used", 0), target_level)
        await sessions_col.update_one(
            {"_id": session_id},
            {
                "$set": {
                    "current_hint_level": target_level,
                    "hints_used": hints_used
                }
            }
        )

        return {
            "hint_level": target_level,
            "hint_title": hint_titles.get(target_level, "Hint"),
            "hint_text": hint_text,
            "hints_remaining": max(0, 3 - target_level),
            "solution_unlocked": session.get("solution_unlocked", False)
        }

    @classmethod
    async def get_solution(cls, user_id: str, session_id: str) -> Dict[str, Any]:
        sessions_col = get_collection("learning_sessions")
        session = await sessions_col.find_one({"_id": session_id})
        if not session:
            session = await sessions_col.find_one({"id": session_id})
        if not session:
            raise EntityNotFoundError("Session not found")

        if session["user_id"] != user_id:
            raise ForbiddenAccessError("Unauthorized access to session")

        # Strict Server-Side Answer Locking Rule
        if not session.get("solution_unlocked", False):
            raise SolutionLockedError(
                "Solution is strictly locked. You must complete your attempts or solve the problem to reveal the official solution."
            )

        problems_col = get_collection("problems")
        problem = await problems_col.find_one({"_id": session["problem_id"]})
        if not problem:
            problem = await problems_col.find_one({"id": session["problem_id"]})
        if not problem:
            raise EntityNotFoundError("Problem not found")

        reason = "Problem solved successfully" if session.get("status") in ["solved_independently", "solved_with_hints"] else "Unlocked after exhausted attempts"

        return {
            "problem_id": str(problem.get("_id") or problem.get("id")),
            "solution": problem.get("solution", ""),
            "explanation": problem.get("explanation", ""),
            "better_approach": problem.get("better_approach", ""),
            "time_complexity": problem.get("time_complexity", "O(n)"),
            "space_complexity": problem.get("space_complexity", "O(1)"),
            "unlocked_reason": reason
        }

    @classmethod
    async def chat_with_tutor(
        cls,
        user_id: str,
        session_id: Optional[str],
        problem_id: Optional[str],
        code: Optional[str],
        message: str
    ) -> Dict[str, Any]:
        users_col = get_collection("users")
        user = await users_col.find_one({"_id": user_id}) or {}
        learner_profile = await learner_service.get_or_create_profile(user_id)

        problem = None
        if problem_id:
            problems_col = get_collection("problems")
            problem = await problems_col.find_one({"_id": problem_id}) or await problems_col.find_one({"id": problem_id})

        prob_title = problem.get("title", "Custom Problem") if problem else "General Programming"
        prob_topic = problem.get("topic", "General") if problem else "General"

        # Conversation History
        history_text = ""
        conv_col = get_collection("conversations")
        if session_id:
            conv = await conv_col.find_one({"session_id": session_id})
            if conv:
                msgs = conv.get("messages", [])[-6:]
                history_text = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in msgs])

        reply_dto = await gemini_client.chat_with_student(
            student_level=user.get("self_declared_level", "intermediate"),
            strong_topics=learner_profile.get("strong_topics", []),
            weak_topics=learner_profile.get("weak_topics", []),
            recurring_mistakes=learner_profile.get("recurring_mistakes", {}),
            problem_title=prob_title,
            problem_topic=prob_topic,
            student_code=code or "# No code provided",
            conversation_history=history_text,
            student_message=message
        )

        if session_id:
            await conv_col.update_one(
                {"session_id": session_id},
                {
                    "$setOnInsert": {
                        "_id": str(uuid.uuid4()),
                        "id": str(uuid.uuid4()),
                        "session_id": session_id,
                        "user_id": user_id,
                        "problem_id": problem_id or "",
                        "created_at": datetime.now(timezone.utc)
                    },
                    "$push": {
                        "messages": {
                            "$each": [
                                {"role": "student", "content": message, "timestamp": datetime.now(timezone.utc)},
                                {"role": "tutor", "content": reply_dto.reply, "timestamp": datetime.now(timezone.utc)}
                            ]
                        }
                    },
                    "$set": {"updated_at": datetime.now(timezone.utc)}
                },
                upsert=True
            )

        return {
            "reply": reply_dto.reply,
            "suggested_followups": reply_dto.suggested_followups,
            "concept": reply_dto.concept
        }

    @classmethod
    async def analyze_custom_problem(
        cls,
        user_id: str,
        problem_title: str,
        problem_description: str,
        student_code: str,
        language: str = "python",
        hint_level: int = 1
    ) -> Dict[str, Any]:
        exec_result = await SafeCodeRunner.run_code(code=student_code, test_cases=[])
        users_col = get_collection("users")
        user = await users_col.find_one({"_id": user_id}) or {}
        learner_profile = await learner_service.get_or_create_profile(user_id)
        student_context = StudentContextBuilder.build_compact_context(user, learner_profile)

        mock_prob = {
            "title": problem_title,
            "description": problem_description,
            "topic": "Custom Problem",
            "subconcept": "logic",
            "difficulty": "intermediate"
        }

        tutor_analysis = await gemini_client.analyze_code(
            student_context=student_context,
            problem=mock_prob,
            student_code=student_code,
            execution_result=exec_result.to_dict(),
            attempt_number=hint_level,
            attempts_allowed=3,
            hint_level=hint_level,
            solution_unlocked=False
        )

        return {
            "is_correct": tutor_analysis.correct,
            "error_type": tutor_analysis.error_type,
            "concept": tutor_analysis.concept,
            "misconception": tutor_analysis.misconception,
            "analysis": tutor_analysis.analysis,
            "hint": tutor_analysis.hint or "Check your logic step-by-step.",
            "hint_level": hint_level,
            "learning_tip": tutor_analysis.learning_tip
        }

tutor_service = TutorOrchestratorService()
