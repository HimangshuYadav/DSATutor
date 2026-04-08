from pydantic import BaseModel, Field
from typing import List, Optional

class TutorObservation(BaseModel):
    """Represents the student's current view of the tutoring session."""
    current_problem: str = Field(..., description="Details and prompt of the current task")
    difficulty: int = Field(..., description="0: Easy, 1: Medium, 2: Hard")
    feedback_summary: str = Field(..., description="Reflective feedback on the student's last submission")
    score: float = Field(0.0, description="Correctness score of the last submission (0 to 1)")
    done: bool = Field(False, description="Whether the current learning objective is met")
    reward: float = Field(0.0, description="The RL reward signal for the last action taken")

class TutorAction(BaseModel):
    """Represents an instructional action taken by the tutor or an agent."""
    action_type: str = Field(..., description="suggest_problem | evaluate_code | adjust_difficulty")
    code_string: Optional[str] = Field(None, description="The code content for evaluation")
    language: str = Field("python", description="The programming language of the code")
    difficulty: Optional[int] = Field(None, description="Target difficulty for problem suggestion")
    adjustment: Optional[str] = Field(None, description="Direction to adjust difficulty: 'up' or 'down'")

class SessionRecord(BaseModel):
    """Internal state tracking for the tutoring session."""
    user_level: int = 0
    success_rate: float = 0.0
    streak: int = 0
    attempts_count: int = 0
    historical_scores: List[float] = []

class CodeSubmission(BaseModel):
    """A direct student submission for evaluation."""
    code: str
    problem: str
    language: str = "python"
