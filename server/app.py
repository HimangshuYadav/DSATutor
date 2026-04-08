import os
import uvicorn
import logging
from fastapi import FastAPI, HTTPException
from .models import TutorObservation, TutorAction, CodeSubmission
from .env import TutorEngine
from .deterministic_grader import grade_deterministic, FIXED_TASKS

# Initialize logging for transparency
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DSATutor Benchmark",
    description="Adaptive Learning Environment for Data Structures and Algorithms."
)

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

def main():
    """Entry point for running the tutor server."""
    port = int(os.getenv("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)

if __name__ == "__main__":
    main()
