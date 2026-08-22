import logging
import json
import re
from typing import Optional, Dict, Any, List
from app.core.config import settings
from app.ai.schemas import TutorAnalysis, ConversationReply, KnowledgeGapExplanation
from app.ai.prompts import (
    SYSTEM_TUTOR_PROMPT,
    DIAGNOSIS_PROMPT_TEMPLATE,
    CONVERSATION_PROMPT_TEMPLATE,
    ASSESSMENT_GAP_PROMPT_TEMPLATE,
    RECOMMENDATION_EXPLANATION_PROMPT_TEMPLATE
)

logger = logging.getLogger("codementor.ai")

class GeminiTutorClient:
    def __init__(self):
        self.model_name = settings.GEMINI_MODEL or "gemini-3.7-flash"
        self._client = None

    def _get_client(self):
        if self._client is None and settings.is_gemini_configured:
            try:
                from google import genai
                self._client = genai.Client(api_key=settings.GEMINI_API_KEY)
            except Exception as e:
                logger.warning(f"Failed to initialize google-genai client: {e}")
                self._client = None
        return self._client

    async def analyze_code(
        self,
        student_context: str,
        problem: Dict[str, Any],
        student_code: str,
        execution_result: Dict[str, Any],
        attempt_number: int,
        attempts_allowed: int,
        hint_level: int,
        solution_unlocked: bool
    ) -> TutorAnalysis:
        test_results = execution_result.get("test_results", [])
        passed_cnt = execution_result.get("passed_count", 0)
        total_cnt = execution_result.get("total_count", len(test_results))
        exec_success = execution_result.get("success", False)
        stderr_text = execution_result.get("stderr", "")

        test_summary = f"{passed_cnt}/{total_cnt} test cases passed."
        if test_results:
            failed_cases = [tc for tc in test_results if not tc.get("passed", False)]
            if failed_cases:
                first_fail = failed_cases[0]
                test_summary += f" First failing case: expected {first_fail.get('expected_output')}, got {first_fail.get('actual_output')}."

        prompt = DIAGNOSIS_PROMPT_TEMPLATE.format(
            student_context=student_context,
            problem_title=problem.get("title", ""),
            problem_topic=problem.get("topic", "General"),
            problem_subconcept=problem.get("subconcept", "general"),
            problem_difficulty=problem.get("difficulty", "intermediate"),
            problem_description=problem.get("description", ""),
            execution_success=exec_success,
            stderr=stderr_text or "None",
            test_results_summary=test_summary,
            student_code=student_code,
            attempt_number=attempt_number,
            attempts_allowed=attempts_allowed,
            hint_level=hint_level,
            solution_unlocked=solution_unlocked
        )

        client = self._get_client()
        if client:
            try:
                from google.genai import types
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_TUTOR_PROMPT,
                        response_mime_type="application/json",
                        response_schema=TutorAnalysis,
                        temperature=0.2,
                    ),
                )
                if response and response.text:
                    parsed_data = json.loads(response.text)
                    return TutorAnalysis.model_validate(parsed_data)
            except Exception as e:
                logger.warning(f"Gemini API call failed: {e}. Falling back to deterministic pedagogical tutor.")

        # High-Quality Fallback Engine
        return self._generate_fallback_analysis(
            problem=problem,
            student_code=student_code,
            execution_result=execution_result,
            hint_level=hint_level,
            solution_unlocked=solution_unlocked
        )

    def _generate_fallback_analysis(
        self,
        problem: Dict[str, Any],
        student_code: str,
        execution_result: Dict[str, Any],
        hint_level: int,
        solution_unlocked: bool
    ) -> TutorAnalysis:
        topic = problem.get("topic", "General")
        subconcept = problem.get("subconcept", "logic")
        is_correct = execution_result.get("success", False)
        stderr_text = execution_result.get("stderr", "")
        error_type = execution_result.get("error_type", "LOGICAL_ERROR")

        if is_correct:
            return TutorAnalysis(
                correct=True,
                error_type="CORRECT",
                concept=topic.lower(),
                subconcept=subconcept,
                misconception=None,
                analysis=f"Outstanding work! Your solution correctly solves '{problem.get('title')}' by handling the problem constraints effectively.",
                hint=None,
                hint_level=hint_level,
                better_approach=problem.get("better_approach"),
                time_complexity=problem.get("time_complexity", "O(n)"),
                space_complexity=problem.get("space_complexity", "O(1)"),
                learning_tip=f"Reflect on how your approach would scale if the input data was 1000x larger."
            )

        # Detect specific misconceptions from code & error
        misconception = None
        has_recursion_err = (
            "RecursionError" in stderr_text
            or "maximum recursion depth" in stderr_text
            or any("RecursionError" in str(tc.get("actual_output", "")) for tc in execution_result.get("test_results", []))
            or (topic.lower() == "recursion" and ("if" not in student_code or ("<=" not in student_code and "==" not in student_code and "<" not in student_code)))
        )
        if has_recursion_err:
            error_type = "RUNTIME_ERROR"
            misconception = "missing_base_case"
            level1_hint = "What condition tells the recursive function to stop calling itself and return a base value?"
            level2_hint = "Without a base case (e.g. `if n <= 1: return 1`), the function recurses indefinitely until the stack overflows."
            level3_hint = "Add a base case check at the very beginning of your function before making the recursive call."
        elif "SyntaxError" in stderr_text:
            error_type = "SYNTAX_ERROR"
            misconception = "syntax_formatting"
            level1_hint = "Check your indentation, colons after statement headers, and matching parentheses."
            level2_hint = "Python relies on indentation and colons (:) to define blocks of code."
            level3_hint = f"Review the syntax error details: {stderr_text.splitlines()[-1] if stderr_text else ''}"
        elif "range(" in student_code and ("len(" in student_code or "1" in student_code):
            error_type = "LOGICAL_ERROR"
            misconception = "loop_boundary_or_indexing"
            level1_hint = "What exact values does your loop counter iterate through on the first and last iteration?"
            level2_hint = "Remember that Python `range(start, stop)` stops strictly before `stop`, and lists are 0-indexed."
            level3_hint = "Check your loop upper limit and index offsets to prevent off-by-one errors."
        else:
            error_type = "LOGICAL_ERROR"
            misconception = f"{topic.lower()}_logic_gap"
            level1_hint = "Trace your code with a small sample input on paper. Does each step do what you expect?"
            level2_hint = f"Focus on how {topic} operates on the input data to reach the target condition."
            level3_hint = f"Verify how your function produces its final return value across all branches."

        # Select hint by level
        if hint_level == 1:
            active_hint = level1_hint
        elif hint_level == 2:
            active_hint = level2_hint
        else:
            active_hint = level3_hint

        return TutorAnalysis(
            correct=False,
            error_type=error_type,
            concept=topic.lower(),
            subconcept=subconcept,
            misconception=misconception,
            analysis=f"Your code encountered an issue with {topic.lower()} ({subconcept}). Let's work through it step by step.",
            hint=active_hint,
            hint_level=hint_level,
            better_approach=problem.get("better_approach") if solution_unlocked else None,
            time_complexity=problem.get("time_complexity") if solution_unlocked else None,
            space_complexity=problem.get("space_complexity") if solution_unlocked else None,
            learning_tip="Notice the pattern between the problem requirements and your state transitions."
        )

    async def chat_with_student(
        self,
        student_level: str,
        strong_topics: List[str],
        weak_topics: List[str],
        recurring_mistakes: Dict[str, int],
        problem_title: str,
        problem_topic: str,
        student_code: str,
        conversation_history: str,
        student_message: str
    ) -> ConversationReply:
        prompt = CONVERSATION_PROMPT_TEMPLATE.format(
            student_level=student_level,
            strong_topics=", ".join(strong_topics) or "None",
            weak_topics=", ".join(weak_topics) or "None",
            recurring_mistakes=str(recurring_mistakes),
            problem_title=problem_title,
            problem_topic=problem_topic,
            student_code=student_code,
            conversation_history=conversation_history,
            student_message=student_message
        )

        client = self._get_client()
        if client:
            try:
                from google.genai import types
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_TUTOR_PROMPT,
                        response_mime_type="application/json",
                        response_schema=ConversationReply,
                        temperature=0.3,
                    ),
                )
                if response and response.text:
                    parsed_data = json.loads(response.text)
                    return ConversationReply.model_validate(parsed_data)
            except Exception as e:
                logger.warning(f"Gemini Chat call failed: {e}. Using fallback.")

        # Pedagogical Fallback reply
        return ConversationReply(
            reply=f"That's a great question about {problem_topic}. When working through '{problem_title}', consider how data transforms step by step. What happens to your variables on the very first iteration or base step?",
            suggested_followups=[
                "Why is my base case condition important?",
                "Can you walk me through a small trace with n = 3?",
                "How does the time complexity change with this approach?"
            ],
            concept=problem_topic.lower()
        )

    async def explain_assessment_gap(
        self,
        self_level: str,
        languages: List[str],
        score_percentage: int,
        correct_count: int,
        total_count: int,
        calculated_level: str,
        topic_scores: Dict[str, float],
        strong_topics: List[str],
        weak_topics: List[str]
    ) -> KnowledgeGapExplanation:
        topic_scores_text = "\n".join([f"- {t}: {int(s * 100)}%" for t, s in topic_scores.items()])
        prompt = ASSESSMENT_GAP_PROMPT_TEMPLATE.format(
            self_level=self_level.capitalize(),
            languages=", ".join(languages),
            score_percentage=score_percentage,
            correct_count=correct_count,
            total_count=total_count,
            calculated_level=calculated_level.capitalize(),
            topic_scores_text=topic_scores_text,
            strong_topics=", ".join(strong_topics) or "None",
            weak_topics=", ".join(weak_topics) or "None"
        )

        client = self._get_client()
        if client:
            try:
                from google.genai import types
                response = client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction="You are CodeMentor AI. Provide clear, encouraging pedagogical evaluation of the student's baseline assessment.",
                        response_mime_type="application/json",
                        response_schema=KnowledgeGapExplanation,
                        temperature=0.2,
                    ),
                )
                if response and response.text:
                    parsed_data = json.loads(response.text)
                    return KnowledgeGapExplanation.model_validate(parsed_data)
            except Exception as e:
                logger.warning(f"Gemini Gap explanation failed: {e}. Using fallback.")

        # High-Quality Fallback
        strong_str = ", ".join(strong_topics) if strong_topics else "general concepts"
        weak_str = ", ".join(weak_topics) if weak_topics else "more advanced topics"
        
        gap_summary = (
            f"You self-declared as {self_level.capitalize()}, and scored {score_percentage}% on the Knowledge Check "
            f"(assessed level: {calculated_level.capitalize()})."
        )
        if self_level.lower() == calculated_level.lower():
            gap_summary += " Your self-assessment is well aligned with your verified diagnostic performance!"
        elif "beginner" in calculated_level.lower() and "intermediate" in self_level.lower():
            gap_summary += f" You have strong intuitive grasp in {strong_str}, but specific gaps in {weak_str} indicate starting with foundational practice will accelerate your growth."
        else:
            gap_summary += f" Your test results highlight mastery in {strong_str} with growth opportunities in {weak_str}."

        return KnowledgeGapExplanation(
            gap_summary=gap_summary,
            strong_topics_analysis=f"Solid foundational performance demonstrated in {strong_str}.",
            weak_topics_analysis=f"Priority focus recommended in {weak_str} to strengthen your core mental models.",
            learning_path_recommendation=f"Start with curated exercises targeting {weak_str} before moving to multi-concept algorithmic challenges."
        )

gemini_client = GeminiTutorClient()
