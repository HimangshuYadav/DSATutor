import os
import uvicorn
import logging
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .models import TutorObservation, TutorAction, SessionRecord, CodeSubmission
from .env import TutorEngine
from .deterministic_grader import grade_deterministic, FIXED_TASKS

# Initialize logging for transparency
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DSATutor Benchmark",
    description="Adaptive Learning Environment for Data Structures and Algorithms."
)

# Mount the frontend directory for static assets (styles, images, scripts)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
async def serve_ui():
    """Serves the main tutoring interface."""
    return FileResponse("frontend/index.html")

# Shared tutoring engine instance
engine = TutorEngine()

@app.post("/reset")
async def reset_session():
    """Initializes or resets the student's tutoring session."""
    return engine.reset()

@app.post("/step")
async def execute_step(action: TutorAction):
    """Processes an action and returns updated progress."""
    obs, reward, done, info = engine.step(action)
    return obs

@app.get("/state")
async def get_session_record():
    """Retrieves the current session progress and statistics."""
    return engine.session

@app.get("/metadata")
async def get_benchmark_metadata():
    """Returns details about available tasks and benchmark version."""
    return {
        "engine": "DSATutor-v1",
        "humanized": True,
        "standard": "OpenEnv-1.0",
        "tasks": [t["info"] for t in FIXED_TASKS]
    }

@app.post("/api/grade_deterministic")
async def run_benchmark_grading(submission: CodeSubmission):
    """Internal grading endpoint for standardized performance benchmarks."""
    matched_task_id = None
    for task in FIXED_TASKS:
        if task["info"]["title"] == submission.problem:
            matched_task_id = task["info"]["id"]
            break
            
    if not matched_task_id:
        raise HTTPException(status_code=404, detail="Requested problem not in standard bank")

    # Grading Debug Log
    logger.info(f"Grading submission for {submission.problem}")
    
    return grade_deterministic(submission.code, matched_task_id)

# ── FRONTEND BRIDGING ROUTES ──────────────────────────────────────

@app.post("/api/setup")
async def frontend_setup():
    """Stub for frontend setup initialization."""
    return {"status": "ok"}

@app.post("/api/assessment")
async def frontend_assessment():
    """Stub for frontend assessment completion."""
    return {"status": "ok"}

@app.get("/api/problem")
async def get_current_problem():
    """Returns the current problem details for the frontend UI."""
    return {
        "problem": {
            "title": engine.current_problem["title"],
            "description": engine.current_problem["prompt"],
            "expected_complexity": engine.current_problem.get("complexity", "O(?)")
        },
        "level": engine.difficulty_level
    }

@app.post("/api/run")
async def run_code(submission: CodeSubmission):
    """Main execution point for the UI playground."""
    action = TutorAction(
        action_type="evaluate_code",
        code_string=submission.code,
        language=submission.language
    )
    obs, reward, done, info = engine.step(action)
    
    return {
        "observation": obs,
        "reward": {"value": min(reward, 1.0)},
        "state": engine.session,
        "done": done,
        "info": info
    }

@app.get("/api/progress")
async def get_progress():
    """Provides data for the frontend Chart.js visualization."""
    return {
        "attempts": list(range(1, len(engine.session.historical_scores) + 1)),
        "scores": engine.session.historical_scores
    }

@app.post("/api/skip")
async def skip_problem():
    """Triggers a problem change from the UI."""
    action = TutorAction(action_type="suggest_problem")
    obs, reward, done, info = engine.step(action)
    
    return {
        "problem": {
            "title": engine.current_problem["title"],
            "description": engine.current_problem["prompt"],
            "expected_complexity": engine.current_problem.get("complexity", "O(?)")
        },
        "level": engine.difficulty_level,
        "state": engine.session,
        "observation": obs,
        "reward": {"value": reward}
    }

# ──────────────────────────────────────────────────────────────────

def main():
    """Entry point for running the tutor server."""
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
