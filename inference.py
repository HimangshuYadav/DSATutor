"""
Inference Script for DSATutor
===================================
MANDATORY
- Before submitting, ensure the following variables are defined:
    API_BASE_URL   The API endpoint for the LLM.
    MODEL_NAME     The model identifier to use.
    HF_TOKEN       Your Hugging Face / API key.
    LOCAL_IMAGE_NAME (Optional) The name of the local image if using Docker.
"""

import asyncio
import os
import httpx
import logging
from typing import List, Optional
from openai import OpenAI

# ── Logging Suppression ──────────────────────────────────────────
# Ensure ONLY the mandated [START], [STEP], and [END] tags hit stdout
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)

# ── Environment Configuration ─────────────────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL") or "https://api.groq.com/openai/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "llama-3.3-70b-versatile"
HF_TOKEN = os.getenv("HF_TOKEN") or os.getenv("GROQ_API_KEY") 
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")
ENV_URL = os.getenv("ENV_URL", "http://127.0.0.1:7860")

MAX_STEPS = 1
TEMPERATURE = 0.1
SUCCESS_SCORE_THRESHOLD = 0.9

TASKS = [
    {"title": "Two Sum", "prompt": "Implement Two Sum in Python. Define `two_sum(nums, target)`. Return ONLY code."},
    {"title": "Longest Increasing Subsequence", "prompt": "Implement LIS in Python. Define `lis_length(nums)`. Return ONLY code."},
    {"title": "Number of Islands", "prompt": "Implement Number of Islands in Python. Define `num_islands(grid)`. Return ONLY code."},
    {"title": "Valid Parentheses", "prompt": "Implement Valid Parentheses in Python. Define `is_valid(s)`. Return ONLY code."},
    {"title": "Merge K Sorted Lists", "prompt": "Implement Merge K Sorted Lists in Python. Define `merge_k_lists(lists)`. Return ONLY code."},
]

# ── Logging Helpers (STDOUT FORMAT) ──────────────────────────────
def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

# ── Inference Logic ──────────────────────────────────────────────
def get_model_message(client: OpenAI, prompt: str) -> str:
    """Invokes the LLM to generate an algorithmic solution."""
    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=TEMPERATURE,
            stream=False,
        )
        content = (completion.choices[0].message.content or "").strip()
        
        if "```python" in content:
            return content.split("```python")[1].split("```")[0].strip()
        elif "```" in content:
            return content.split("```")[1].split("```")[0].strip()
        return content
    except Exception as exc:
        return f"# Model request failed: {exc}"

async def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

    async with httpx.AsyncClient(base_url=ENV_URL, timeout=60.0) as session:
        for task in TASKS:
            rewards = []
            steps_taken = 0
            score = 0.0
            success = False
            
            log_start(task=task["title"], env="DSATutor", model=MODEL_NAME)

            try:
                await session.post("/reset")
                
                for step in range(1, MAX_STEPS + 1):
                    solution = get_model_message(client, task["prompt"])
                    
                    response = await session.post("/api/grade_deterministic", json={
                        "code": solution,
                        "problem": task["title"]
                    })
                    
                    if response.status_code == 200:
                        data = response.json()
                        reward = data.get("score", 0.0)
                        done = (reward >= SUCCESS_SCORE_THRESHOLD)
                    else:
                        reward = 0.0
                        done = True

                    rewards.append(reward)
                    steps_taken = step
                    
                    log_step(step=step, action="solve", reward=reward, done=done, error=None)
                    
                    if done:
                        break

                score = sum(rewards) / len(rewards) if rewards else 0.0
                success = score >= SUCCESS_SCORE_THRESHOLD

            finally:
                log_end(success=success, steps=steps_taken, score=score, rewards=rewards)

if __name__ == "__main__":
    asyncio.run(main())
