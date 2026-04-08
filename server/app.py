"""
DSATutor API Server.
Main entry point for both the OpenEnv evaluation agent and the Student UI.
"""

import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .env import TutorEngine
from .models import TutorAction, TutorObservation, SessionRecord
from .models import UserSetupRequest, CodeSubmission, SetupAssessmentRequest
from .tasks import get_task_by_difficulty
from .deterministic_grader import FIXED_TASKS, grade_deterministic

app = FastAPI(
    title="DSATutor API",
    description="Intelligent DSA Tutoring through Reinforcement Learning",
)

# Shared tutoring engine
engine = TutorEngine()

# --- OpenEnv Evaluator Endpoints ---

@app.post("/reset")
async def initialize_session():
    """Initializes a new student session."""
    observation = engine.reset()
    return observation.dict()

@app.post("/step")
async def handle_step(action: TutorAction):
    """Processes a student action and returns the outcome."""
    observation = engine.step(action)
    return observation.dict()

@app.get("/state")
async def fetch_current_state():
    """Returns the full internal session data."""
    return engine.state.dict()

@app.get("/metadata")
async def fetch_metadata():
    """Returns environment specification details."""
    meta = engine.get_metadata()
    return {
        "name": meta.name,
        "description": meta.description,
        "version": meta.version,
    }

# --- Student UI & Client Endpoints ---

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def serve_ui():
    """Serves the main tutoring dashboard."""
    return FileResponse("frontend/index.html")

@app.post("/api/setup")
async def configure_profile(config: UserSetupRequest):
    """Sets preferred topics for the student profile."""
    engine.state.selected_topics = config.topics
    return {"status": "configured", "state": engine.state.dict()}

@app.post("/api/assessment")
async def evaluate_proficiency(assessment: SetupAssessmentRequest):
    """Sets initial difficulty based on diagnostic test results."""
    if assessment.score >= 0.8:
        level = 2
    elif assessment.score >= 0.5:
        level = 1
    else:
        level = 0
    engine.state.user_level = level
    return {"success": True, "starting_level": level}

@app.get("/api/problem")
async def fetch_problem():
    """Retrieves the current problem or loads a new one if needed."""
    if not engine.current_problem:
        engine.current_problem = get_task_by_difficulty(
            engine.state.user_level,
            active_topics=engine.state.selected_topics,
            used_ids=engine.state.past_problem_ids,
        )
        engine.state.past_problem_ids.append(engine.current_problem["id"])
    
    return {
        "problem": engine.current_problem,
        "current_level": engine.state.user_level,
    }

@app.post("/api/skip")
async def skip_problem():
    """Skips the active problem (user-initiated)."""
    action = TutorAction(action_type="suggest_problem")
    observation = engine.step(action)
    return {
        "problem": engine.current_problem,
        "current_level": engine.state.user_level,
        "observation": observation.dict(),
        "reward_info": observation.metadata.get("reason", ""),
        "state": engine.state.dict(),
    }

@app.post("/api/run")
async def submit_submission(submission: CodeSubmission):
    """Evaluates student code submission."""
    action = TutorAction(
        action_type="evaluate_code",
        code_string=submission.code,
        language=submission.language,
    )
    observation = engine.step(action)
    return {
        "observation": observation.dict(),
        "feedback": observation.feedback_summary,
        "is_solved": observation.done,
        "state": engine.state.dict(),
        "next_problem": engine.current_problem,
    }

@app.get("/api/progress")
async def get_performance_stats():
    """Returns historical scores for analytics and visualization."""
    data = engine.state
    indices = list(range(1, len(data.historical_scores) + 1))
    return {"labels": indices, "scores": data.historical_scores}

# --- Deterministic Grading (Reserved for Evaluator) ---

@app.get("/api/tasks")
async def get_task_benchmarks():
    """Lists tasks with deterministic test harnesses."""
    return {"tasks": [t["info"] for t in FIXED_TASKS]}

@app.post("/api/grade_deterministic")
async def run_benchmark_grading(submission: CodeSubmission):
    """Executes deterministic test cases against student code."""
    matched_task_id = None
    for task in FIXED_TASKS:
        if task["info"]["title"] == submission.problem:
            matched_task_id = task["info"]["id"]
            break

    if not matched_task_id:
        return {"error": f"Benchmark not found for: {submission.problem}"}

    grading_result = grade_deterministic(submission.code, matched_task_id)
    return {
        "correctness": grading_result["correctness"],
        "cases_passed": grading_result["passed"],
        "cases_total": grading_result["total"],
        "tutor_feedback": grading_result["feedback"],
        "traceback": grading_result["errors"],
    }

def main():
    """Starts the API server with settings from the environment."""
    run_port = int(os.getenv("PORT", 7860))
    print(f"Server initializing on port {run_port}...")
    uvicorn.run(app, host="0.0.0.0", port=run_port)

if __name__ == "__main__":
    main()
