"""
Data models for the DSATutor environment.
These models define the communication contract between the tutor and the agent.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from openenv.core.env_server import (
    Action as BaseAction,
    Observation as BaseObservation,
)

class TutorObservation(BaseObservation):
    """Data returned to the student after each interaction."""
    current_problem: str = ""
    difficulty: int = 0
    feedback_summary: str = ""
    score: float = 0.0
    next_recommendation_hint: str = ""

class TutorAction(BaseAction):
    """Actions the student or automated agent can take."""
    action_type: str = Field(
        ..., description="Type of action: suggest_problem, evaluate_code, or adjust_difficulty"
    )
    difficulty: Optional[int] = None
    topic: Optional[str] = None
    code_string: Optional[str] = None
    language: Optional[str] = "python"
    adjustment: Optional[str] = Field(None, description="Tweak level: up, down, or same")

class SessionRecord(BaseModel):
    """Internal state tracking for the current tutoring session."""
    user_level: int = 0
    selected_topics: List[str] = []
    last_problem_difficulty: int = 0
    success_rate: float = 0.0
    streak: int = 0
    last_feedback_score: float = 0.0
    attempts_count: int = 0
    historical_scores: List[float] = []
    past_problem_ids: List[str] = []
    max_score_this_episode: float = 0.0
    last_code_submitted: str = ""

class Reward(BaseModel):
    """Helper for passing reward values and their context."""
    value: float
    reason: str

class CodeSubmission(BaseModel):
    """Payload for submitting code to the tutor's grading engine."""
    code: str
    problem: str
    language: str = "python"

class UserSetupRequest(BaseModel):
    """Initial configuration for a new student session."""
    topics: List[str]

class SetupAssessmentRequest(BaseModel):
    """Result of the initial proficiency assessment."""
    score: float
