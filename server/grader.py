"""
Grading engine for mapping AI assessments to reinforcement learning rewards.
This module classifies code quality into structured reward tiers.
"""

from .gemini_client import evaluate_with_ai
from .models import Reward

def evaluate_student_code(
    code: str, 
    problem: dict, 
    previous_score: float,
    language: str = "python"
) -> tuple:
    """
    Evaluates submission quality using AI analysis.
    Returns: (Reward, final_score, feedback, is_limited, retry_after)
    """
    # Guard against empty submissions
    if not code or not code.strip():
        return (
            Reward(value=0.0, reason="Empty submission"),
            0.0, 
            "Nothing submitted yet. Let's start with some code!", 
            False, 
            0
        )

    # Perform AI-based structural and logic analysis
    report = evaluate_with_ai(code, problem, language)

    # Handle service availability
    if report.get("_rate_limited", False):
        return (
            Reward(value=0.0, reason="Service temporarily limited"),
            0.0, 
            report["feedback_summary"], 
            True, 
            report.get("_retry_after", 0)
        )

    # Extract metrics from the evaluation report
    quality_score = float(report.get("correctness", 0.0))
    detected_complexity = report.get("complexity", "unknown")
    tutor_feedback = report.get("feedback_summary", "Review your implementation for logic gaps.")
    target_complexity = problem.get("expected_complexity", "")

    justifications = []

    # Tiered Reward Mapping
    # Tier 1: Incorrect or bugged (Score < 0.5)
    if quality_score < 0.5:
        base_reward = quality_score * 0.8  # Maps 0.0-0.49 to 0.0-0.39
        justifications.append("Logic contains bugs or misses test cases")

    # Tier 2: Correct but suboptimal (Score 0.5 - 0.79)
    elif quality_score < 0.8:
        base_reward = 0.5 + (quality_score - 0.5)
        justifications.append("Correct implementation")
        if target_complexity and target_complexity not in detected_complexity:
            justifications.append(f"Efficiency goal missed (Target: {target_complexity})")

    # Tier 3: High quality (Score 0.8 - 0.89)
    elif quality_score < 0.9:
        base_reward = 0.8 + (quality_score - 0.8)
        justifications.append("High-quality solution")
        if target_complexity and target_complexity in detected_complexity:
            justifications.append(f"Optimal complexity ({target_complexity})")

    # Tier 4: Mastered (Score 0.9+)
    else:
        base_reward = 0.9 + (quality_score - 0.9)
        justifications.append("Exceptional — handled edge cases and performance goals")
        if target_complexity and target_complexity in detected_complexity:
            justifications.append("Optimal implementation achieved")

    # Incremental progress bonus
    if previous_score > 0 and quality_score > previous_score + 0.1:
        base_reward = min(base_reward + 0.05, 1.0)
        justifications.append("Significant improvement over previous attempt")

    final_reward = round(max(0.0, min(1.0, base_reward)), 2)

    return (
        Reward(value=final_reward, reason=", ".join(justifications)),
        final_reward, 
        tutor_feedback, 
        False, 
        0
    )
