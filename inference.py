"""
Baseline Agent for DSATutor Benchmarking.
Uses an LLM to generate solutions and evaluates them using the tutor server.
"""

import asyncio
import os
import httpx
import logging
from typing import List, Optional
from openai import OpenAI

# Environment configuration
API_BASE = os.getenv("API_BASE_URL", "https://api.groq.com/openai/v1")
MODEL = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
TOKEN = os.getenv("HF_TOKEN") or os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY")
TARGET_URL = os.getenv("ENV_URL", "http://127.0.0.1:7860")

# Setup clean logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Standard OpenEnv Logging Helpers
def log_start(task: str, env: str, model: str):
    logger.info(f"[START] task={task} env={env} model={model}")

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    logger.info(f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={error or 'null'}")

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    logger.info(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={','.join(f'{r:.2f}' for r in rewards)}")

# Task configuration for the agent
TASKS = [
    {"title": "Two Sum", "prompt": "Implement Two Sum in Python. Define `two_sum(nums, target)`. Return ONLY code."},
    {"title": "Longest Increasing Subsequence", "prompt": "Implement LIS in Python. Define `lis_length(nums)`. Return ONLY code."},
    {"title": "Number of Islands", "prompt": "Implement Number of Islands in Python. Define `num_islands(grid)`. Return ONLY code."},
    {"title": "Valid Parentheses", "prompt": "Implement Valid Parentheses in Python. Define `is_valid(s)`. Return ONLY code."},
    {"title": "Merge K Sorted Lists", "prompt": "Implement Merge K Sorted Lists in Python. Define `merge_k_lists(lists)`. Return ONLY code."},
]

async def generate_code(prompt: str) -> str:
    """Invokes the LLM to generate an algorithmic solution."""
    try:
        # Use OpenAI-style client
        client = OpenAI(base_url=API_BASE, api_key=TOKEN)
        completion = await asyncio.to_thread(
            client.chat.completions.create,
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        content = completion.choices[0].message.content or ""
        # Precise code extraction
        if "```python" in content:
            return content.split("```python")[1].split("```")[0].strip()
        elif "```" in content:
            return content.split("```")[1].split("```")[0].strip()
        return content.strip()
    except Exception as e:
        return f"# LLM Error: {e}"

async def evaluate_tasks():
    """Main loop to evaluate the agent across standard tasks."""
    async with httpx.AsyncClient(base_url=TARGET_URL, timeout=60.0) as session:
        for task in TASKS:
            log_start(task=task["title"], env="DSATutor", model=MODEL)
            
            try:
                # Prepare environment
                await session.post("/reset")
                
                # Interaction attempt
                solution = await generate_code(task["prompt"])
                
                response = await session.post("/api/grade_deterministic", json={
                    "code": solution,
                    "problem": task["title"]
                })
                
                if response.status_code == 200:
                    data = response.json()
                    reward = data.get("score", 0.0)
                    log_step(step=1, action="solve", reward=reward, done=(reward >= 0.9), error=None)
                    log_end(success=(reward >= 0.9), steps=1, score=reward, rewards=[reward])
                else:
                    log_end(success=False, steps=1, score=0.0, rewards=[0.0])
                    
            except Exception as e:
                logger.error(f"Execution failure: {e}")

if __name__ == "__main__":
    asyncio.run(evaluate_tasks())
