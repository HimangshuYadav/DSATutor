import random
from typing import Tuple, Dict, Any
from .models import TutorObservation, TutorAction, SessionRecord
from .tasks import ALL_TASKS
from .grader import evaluate_student_code

class TutorEngine:
    """Core logic engine for the Adaptive DSA Tutor."""
    
    def __init__(self):
        self.session = SessionRecord()
        self.current_problem = random.choice(ALL_TASKS[0])
        self.difficulty_level = 0
        self.max_steps = 15
        self.step_count = 0

    def reset(self) -> TutorObservation:
        """Starts a fresh tutoring session."""
        self.session = SessionRecord()
        self.current_problem = random.choice(ALL_TASKS[0])
        self.difficulty_level = 0
        self.step_count = 0
        return self._generate_observation("Welcome to DSATutor! Let's build your algorithmic skills.")

    def step(self, action: TutorAction) -> Tuple[TutorObservation, float, bool, Dict]:
        """Executes a single instructional step."""
        self.step_count += 1
        reward = 0.0
        feedback = ""
        done = False

        if action.action_type == "suggest_problem":
            target_diff = action.difficulty if action.difficulty is not None else self.difficulty_level
            self.current_problem = random.choice(ALL_TASKS[target_diff])
            self.difficulty_level = target_diff
            feedback = f"New focus: {self.current_problem['title']}"
            reward = -0.05 # Minor penalty for context switching

        elif action.action_type == "adjust_difficulty":
            if action.adjustment == "up" and self.difficulty_level < 2:
                self.difficulty_level += 1
            elif action.adjustment == "down" and self.difficulty_level > 0:
                self.difficulty_level -= 1
            self.current_problem = random.choice(ALL_TASKS[self.difficulty_level])
            feedback = f"Level adjusted to {self.difficulty_level}. Here's a {self.current_problem['difficulty']} problem."
            reward = 0.0

        elif action.action_type == "evaluate_code":
            if not action.code_string:
                feedback = "Please provide your code for evaluation."
                reward = -0.2
            else:
                result = evaluate_student_code(action.code_string, self.current_problem, action.language)
                score = result["score"]
                feedback = result["feedback"]
                
                # Reward Shaping
                reward = score
                if score >= 0.95:
                    self.session.streak += 1
                    reward += 0.2 # Mastering bonus
                else:
                    self.session.streak = 0
                
                self.session.historical_scores.append(score)
                self.session.success_rate = sum(self.session.historical_scores) / len(self.session.historical_scores)
                self.session.attempts_count += 1

                # Adaptive Advancement
                if self.session.streak >= 2 and self.difficulty_level < 2:
                    self.difficulty_level += 1
                    feedback += " You're on fire! Advancing to the next level."
                elif score < 0.2 and self.difficulty_level > 0:
                    self.difficulty_level -= 1
                    feedback += " This one is tough. Let's practice some fundamentals first."

        # Session Termination
        if self.step_count >= self.max_steps:
            done = True
        if self.session.success_rate > 0.85 and self.session.attempts_count >= 5 and self.difficulty_level == 2:
            done = True
            reward += 10.0 # Goal completion reward

        obs = self._generate_observation(feedback)
        obs.reward = reward
        obs.score = self.session.historical_scores[-1] if self.session.historical_scores else 0.0
        obs.done = done
        
        return obs, reward, done, {}

    def _generate_observation(self, feedback: str) -> TutorObservation:
        """Utility to package the current state into an observation."""
        return TutorObservation(
            current_problem=f"{self.current_problem['title']}: {self.current_problem['prompt']}",
            difficulty=self.difficulty_level,
            feedback_summary=feedback,
            score=self.session.historical_scores[-1] if self.session.historical_scores else 0.0,
            done=False,
            reward=0.0
        )
