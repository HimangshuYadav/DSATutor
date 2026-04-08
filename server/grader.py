from typing import Dict, Any
from .gemini_client import evaluate_with_ai

def evaluate_student_code(code: str, task: Dict[str, Any], language: str = "python") -> Dict[str, Any]:
    """
    Evaluates the correctness and logic of a student's solution.
    Utilizes AI for qualitative analysis and feedback.
    """
    if not code or len(code.strip()) < 10:
        return {
            "score": 0.0,
            "feedback": "Your submission seems incomplete. Please provide a more robust implementation."
        }
    
    # Perform qualitative evaluation via AI
    evaluation = evaluate_with_ai(code, task, language)
    
    raw_score = evaluation.get("correctness", 0.0)
    feedback = evaluation.get("feedback", "Unable to provide specific feedback at this time.")

    # Apply reward-shaping tiers for reinforcement learning stability
    if raw_score >= 0.95:
        final_score = 1.0
    elif raw_score >= 0.75:
        final_score = 0.8
    elif raw_score >= 0.40:
        final_score = 0.5
    else:
        final_score = raw_score
        
    return {
        "score": round(final_score, 2),
        "feedback": feedback
    }
