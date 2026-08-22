from typing import Dict, Any, Optional

class StudentContextBuilder:
    @staticmethod
    def build_compact_context(
        user: Dict[str, Any],
        learner_profile: Optional[Dict[str, Any]] = None,
        recent_attempts: Optional[list] = None
    ) -> str:
        level = user.get("self_declared_level", "intermediate").capitalize()
        profile = learner_profile or {}
        
        strong = ", ".join(profile.get("strong_topics", [])) or "None recorded yet"
        weak = ", ".join(profile.get("weak_topics", [])) or "None recorded yet"
        
        mistakes = profile.get("recurring_mistakes", {})
        top_mistakes = sorted(mistakes.items(), key=lambda x: x[1], reverse=True)[:3]
        mistakes_str = ", ".join([f"{k} ({v}x)" for k, v in top_mistakes]) or "None identified yet"
        
        perf = profile.get("recent_performance", {})
        total_att = perf.get("total_attempts", 0)
        ind_solves = perf.get("independent_solves", 0)
        hint_solves = perf.get("hint_assisted_solves", 0)
        
        context_lines = [
            f"Skill Level: {level}",
            f"Strong Concepts: {strong}",
            f"Weak Concepts: {weak}",
            f"Recurring Misconceptions: {mistakes_str}",
            f"Track Record: {ind_solves} independent solves, {hint_solves} hint-assisted solves out of {total_att} attempts"
        ]
        return "\n".join(context_lines)
