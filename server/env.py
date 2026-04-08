"""
DSATutor Logic Engine.
Manages the state transitions, grading integration, and reward shaping 
for the tutoring session.
"""

from typing import Optional, Any
from openenv.core.env_server import Environment

from .models import TutorObservation, TutorAction, SessionRecord, Reward
from .tasks import get_task_by_difficulty
from .grader import evaluate_student_code

class TutorEngine(Environment[TutorAction, TutorObservation, SessionRecord]):
    """
    Main tutoring engine that implements the OpenEnv specification.
    Coordinates between student actions and the problem/grading systems.
    """

    SUPPORTS_CONCURRENT_SESSIONS = False

    def __init__(self):
        super().__init__()
        self._state = SessionRecord()
        self.current_problem = None
        self._last_feedback = "Welcome to your DSA tutoring session!"

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        **kwargs: Any,
    ) -> TutorObservation:
        """Starts a fresh session with a reset state."""
        self._state = SessionRecord()
        self.current_problem = None
        self._last_feedback = "New session started."
        self._state.max_score_this_episode = 0.0
        self._state.last_code_submitted = ""
        return self._generate_observation()

    @property
    def state(self) -> SessionRecord:
        """Exposes the internal session data."""
        return self._state

    def step(
        self,
        action: TutorAction,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> TutorObservation:
        """Processes a single interaction (Action) and returns the result (Observation)."""
        reward_val = 0.0
        reward_reason = "No action taken"
        is_done = False
        extra_info = {}

        # Handle problem suggestion or skipping
        if action.action_type == "suggest_problem":
            difficulty = action.difficulty if action.difficulty is not None else self._state.user_level
            old_problem_id = self.current_problem["id"] if self.current_problem else None

            self.current_problem = get_task_by_difficulty(
                difficulty,
                exclude_id=old_problem_id,
                active_topics=self._state.selected_topics,
                used_ids=self._state.past_problem_ids,
            )
            self._state.past_problem_ids.append(self.current_problem["id"])
            self._state.last_problem_difficulty = difficulty

            # Penalty for skipping to avoid spamming for easy problems
            reward_val = -0.1
            reward_reason = "Skipped to a new problem"
            self._state.success_rate = max(0.0, self._state.success_rate - 0.05)
            self._state.historical_scores.append(self._state.success_rate)

            if self._state.user_level > 0:
                self._state.user_level -= 1
                self._last_feedback = "Problem skipped. I've adjusted the difficulty down slightly."
            else:
                self._last_feedback = "Problem skipped. Here is a fresh one for you."

        # Handle code evaluation
        elif action.action_type == "evaluate_code":
            if not self.current_problem:
                self.current_problem = get_task_by_difficulty(self._state.user_level)
                self._state.past_problem_ids.append(self.current_problem["id"])

            language = action.language or "python"
            grade, score, feedback, is_limited, retry_time = evaluate_student_code(
                action.code_string,
                self.current_problem,
                self._state.last_feedback_score,
                language,
            )

            # Handle API rate limits gracefully
            if is_limited:
                extra_info["retry_after"] = retry_time
                self._last_feedback = feedback
                observation = self._generate_observation()
                observation.reward = 0.0
                observation.metadata = extra_info
                return observation

            reward_val = grade.value
            reward_reason = grade.reason
            self._state.last_feedback_score = score
            self._state.attempts_count += 1
            self._state.historical_scores.append(score)

            # Reward Shaping: High Score Bonus
            if score > self._state.max_score_this_episode:
                progress_bonus = 0.1
                reward_val = min(1.0, reward_val + progress_bonus)
                reward_reason += f" (+{progress_bonus} improvement bonus)"
                self._state.max_score_this_episode = score
            
            # Reward Shaping: Stagnation Penalty
            if action.code_string == self._state.last_code_submitted:
                repeat_penalty = -0.05
                reward_val = max(-1.0, reward_val + repeat_penalty)
                reward_reason += f" ({repeat_penalty} penalty: no changes detected)"
            
            self._state.last_code_submitted = action.code_string or ""

            # Update moving average success rate
            if self._state.success_rate > 0:
                self._state.success_rate = round(
                    self._state.success_rate * 0.5 + score * 0.5, 2)
            else:
                self._state.success_rate = score

            # Update learning streak
            if score >= 0.5:
                self._state.streak += 1
            else:
                self._state.streak = 0

            self._last_feedback = feedback

            # Automatic level adjustment based on performance
            if self._state.success_rate > 0.7 and self._state.user_level < 2:
                self._state.user_level += 1
                self._last_feedback += " (Level Up! You're doing great. 🎉)"
            elif self._state.success_rate < 0.3 and self._state.user_level > 0:
                self._state.user_level -= 1
                self._last_feedback += " (Difficulty adjusted to help build your base)"

            # Pre-load next problem on successful completion
            if score >= 0.5:
                self.current_problem = get_task_by_difficulty(
                    self._state.user_level,
                    exclude_id=self.current_problem["id"],
                    active_topics=self._state.selected_topics,
                    used_ids=self._state.past_problem_ids,
                )
                self._state.past_problem_ids.append(self.current_problem["id"])
                extra_info["new_problem_revealed"] = self.current_problem

        # Handle manual difficulty adjustment
        elif action.action_type == "adjust_difficulty":
            if action.adjustment == "up" and self._state.user_level < 2:
                self._state.user_level += 1
                reward_val = 0.2
                reward_reason = "Manual level increase"
            elif action.adjustment == "down" and self._state.user_level > 0:
                self._state.user_level -= 1
                reward_val = 0.2
                reward_reason = "Manual level decrease"
            else:
                reward_reason = "Level remained unchanged"

        # Check for environment completion (The 'Done' condition)
        if action.action_type == "evaluate_code":
            if (self._state.user_level == 2
                    and self._state.success_rate >= 0.8
                    and self._state.attempts_count >= 5
                    and self._state.streak >= 3):
                is_done = True
                reward_val = min(1.0, reward_val + 0.5)
                reward_reason += " — Proficiency achieved!"

        # Assemble final observation
        observation = self._generate_observation()
        observation.done = is_done
        observation.reward = round(reward_val, 2)
        observation.metadata = {
            "reason": reward_reason,
            **extra_info,
        }
        return observation

    def _generate_observation(self) -> TutorObservation:
        """Builds a formatted observation from the current state."""
        title = self.current_problem["title"] if self.current_problem else "N/A"
        context_hint = ""
        if self.current_problem:
            context_hint = f"Complexity goal: {self.current_problem.get('expected_complexity', 'Not specified')}"

        return TutorObservation(
            current_problem=title,
            difficulty=self._state.last_problem_difficulty,
            feedback_summary=self._last_feedback,
            score=self._state.last_feedback_score,
            next_recommendation_hint=context_hint,
        )

    def get_metadata(self):
        """Standard OpenEnv metadata."""
        from openenv.core.env_server import EnvironmentMetadata
        return EnvironmentMetadata(
            name="DSATutor",
            description="Intelligent DSA Tutor with Adaptive RL Grading",
            version="2.1.0",
        )
