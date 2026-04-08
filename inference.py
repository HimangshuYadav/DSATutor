"""
Inference Baseline for DSATutor.
Evaluates an LLM-based agent against the deterministic task bank.
Follows the OpenEnv standard logging format.
"""

import asyncio
import os
import httpx
from typing import List, Optional
from openai import OpenAI

# Environment configuration
API_BASE = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
TOKEN = os.getenv("HF_TOKEN") or os.getenv("API_KEY") or os.getenv("GROQ_API_KEY")
TARGET_URL = os.getenv("ENV_URL", "http://127.0.0.1:7860")

# OpenAI client initialization
llm_client = OpenAI(base_url=API_BASE, api_key=TOKEN)

# Standard OpenEnv Logging Format
def log_start(task: str, env: str, model: str):
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]):
    err_str = error if error else "null"
    done_str = str(done).lower()
    print(f"[STEP] step={step} action={action} reward={reward:.2f} done={done_str} error={err_str}", flush=True)

def log_end(success: bool, steps: int, score: float, rewards: List[float]):
    rewards_csv = ",".join(f"{r:.2f}" for r in rewards)
    success_str = str(success).lower()
    print(f"[END] success={success_str} steps={steps} score={score:.3f} rewards={rewards_csv}", flush=True)

# Problem catalog
AGENT_TASKS = [
    {"title": "Two Sum", "prompt": "Solve Two Sum in Python. Define `two_sum(nums, target)`. Return ONLY code."},
    {"title": "Longest Increasing Subsequence", "prompt": "Solve LIS in Python. Define `lis_length(nums)`. Return ONLY code."},
    {"title": "Number of Islands", "prompt": "Solve Number of Islands in Python. Define `num_islands(grid)`. Return ONLY code."},
    {"title": "Valid Parentheses", "prompt": "Solve Valid Parentheses in Python. Define `is_valid(s)`. Return ONLY code."},
    {"title": "Merge K Sorted Lists", "prompt": "Solve Merge K Sorted Lists in Python. Define `merge_k_lists(lists)`. Return ONLY code."},
]

def parse_llm_response(text: str) -> str:
    """Cleans up LLM output to extract pure Python code."""
    if "```python" in text:
        return text.split("```python")[1].split("```")[0].strip()
    if "```" in text:
        return text.split("```")[1].split("```")[0].strip()
    return text.strip()

async def fetch_llm_code(prompt: str) -> str:
    """Asynchronous wrapper for LLM code generation."""
    try:
        completion = await asyncio.to_thread(
            llm_client.chat.completions.create,
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a senior algorithms engineer. Provide concise Python implementations."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=800,
        )
        return parse_llm_response(completion.choices[0].message.content or "")
    except Exception as e:
        return f"# Evaluation Error: {e}"

async def run_evaluation():
    """Main evaluation loop for the baseline agent."""
    async with httpx.AsyncClient(base_url=TARGET_URL, timeout=45.0) as session:
        for task in AGENT_TASKS:
            name = task["title"]
            log_start(task=name, env="DSATutor", model=MODEL)

            episode_rewards = []
            final_step = 0
            is_successful = False
            last_err_msg = "null"

            # Prepare the engine
            try:
                await session.post("/reset")
            except Exception:
                log_end(success=False, steps=0, score=0.0, rewards=[])
                continue

            # Interaction loop
            try:
                for current_step in range(1, 4): # Max 3 attempts
                    final_step = current_step
                    solution_code = await fetch_llm_code(task["prompt"])
                    
                    try:
                        resp = await session.post(
                            "/api/grade_deterministic",
                            json={"code": solution_code, "problem": name}
                        )
                        
                        if resp.status_code == 200:
                            playback = resp.json()
                            reward = playback.get("correctness", 0.0)
                            done = reward >= 0.9
                            last_err_msg = "null"
                        else:
                            reward, done, last_err_msg = 0.0, False, f"server_err_{resp.status_code}"
                    except Exception:
                        reward, done, last_err_msg = 0.0, False, "connection_lost"

                    episode_rewards.append(reward)
                    log_step(step=current_step, action="submit_code", reward=reward, done=done, error=last_err_msg)

                    if done:
                        is_successful = True
                        break
            finally:
                avg_score = sum(episode_rewards) / len(episode_rewards) if episode_rewards else 0.0
                log_end(success=is_successful, steps=final_step, score=avg_score, rewards=episode_rewards)

if __name__ == "__main__":
    asyncio.run(run_evaluation())
