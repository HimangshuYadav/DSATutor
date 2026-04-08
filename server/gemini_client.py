"""
AI Evaluation Client.
Handles the multi-provider fallback logic for grading student code.
Providers (in order): Groq (Llama), Gemini, and a safe local heuristic.
"""

import os
import json
import re

try:
    from groq import Groq
except ImportError:
    Groq = None

try:
    from google import genai
except ImportError:
    genai = None

# --- Configuration ---

GROQ_DEFAULT_MODEL = "llama-3.3-70b-versatile"
GEMINI_DEFAULT_MODEL = "gemini-2.0-flash"

def _get_groq_engine():
    key = os.environ.get("GROQ_API_KEY")
    return Groq(api_key=key) if key and Groq else None

def _get_gemini_engine():
    key = os.environ.get("GEMINI_EVAL_API_KEY") or os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=key) if key and genai else None

# --- Helpers ---

def _clean_json_response(text: str) -> dict:
    """Extracts JSON from common markdown block patterns."""
    text = text.strip()
    patterns = [r"```json", r"```"]
    for p in patterns:
        if text.startswith(p):
            text = text[len(p):]
        if text.endswith("```"):
            text = text[:-3]
    return json.loads(text.strip())

def _construct_tutor_prompt(code: str, task: dict, lang: str) -> str:
    """Builds the grading prompt for the LLM providers."""
    return f"""Evaluate implementation for: "{task['title']}".
Description: {task['description']}
Expected Complexity: {task['expected_complexity']}
Language: {lang}

Code:
```{lang}
{code}
```

Grading Criteria:
1. correctness (0.0-1.0): 0.5+ means correct logic. 0.9+ means optimal and clean.
2. Be strict on performance. If significantly slower than {task['expected_complexity']}, don't exceed 0.8.
3. Feedback: 1-2 sentences on what's failing. Do NOT provide code or specific fixes.

Return a JSON object:
{{
    "correctness": float,
    "complexity": "e.g. O(N)",
    "feedback_summary": "Short critique",
    "optimization_hint": "Vague directional nudge"
}}"""

# --- Provider Implementations ---

def _evaluate_via_groq(code: str, task: dict, lang: str) -> dict | None:
    engine = _get_groq_engine()
    if not engine:
        return None

    try:
        chat = engine.chat.completions.create(
            model=GROQ_DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": "You are a senior algorithms examiner. Return ONLY JSON."},
                {"role": "user", "content": _construct_tutor_prompt(code, task, lang)}
            ],
            temperature=0.2,
            max_tokens=400,
        )
        content = chat.choices[0].message.content.strip()
        data = _clean_json_response(content)
        data.update({"_rate_limited": False, "_provider": "groq"})
        return data
    except Exception as e:
        print(f"Groq provider hint: {e}")
        return None

def _evaluate_via_gemini(code: str, task: dict, lang: str) -> dict | None:
    engine = _get_gemini_engine()
    if not engine:
        return None

    try:
        response = engine.models.generate_content(
            model=GEMINI_DEFAULT_MODEL,
            contents=_construct_tutor_prompt(code, task, lang),
        )
        data = _clean_json_response(response.text.strip())
        data.update({"_rate_limited": False, "_provider": "gemini"})
        return data
    except Exception as e:
        print(f"Gemini provider hint: {e}")
        return None

def calculate_heuristic_grade(code: str, task: dict) -> dict:
    """Fallback grading logic when cloud APIs are unavailable."""
    clean_code = code.strip()
    if len(clean_code) < 10:
        return {
            "correctness": 0.0, "complexity": "N/A",
            "feedback_summary": "Submission is too short to evaluate.",
            "_rate_limited": False,
        }

    # Basic structural check
    has_loop = any(k in clean_code for k in ["for", "while", "forEach", "map"])
    has_func = any(k in clean_code for k in ["def ", "function ", "void "])
    
    score = 0.2
    if has_func: score += 0.1
    if has_loop: score += 0.1
    if len(clean_code) > 100: score += 0.2

    return {
        "correctness": min(0.6, score),
        "complexity": "Analyzed locally",
        "feedback_summary": "Graded locally due to service outage.",
        "_rate_limited": False,
    }

# --- Main Entry Point ---

def evaluate_with_ai(code: str, task: dict, lang: str = "python") -> dict:
    """Primary entry point for grading. Tries Groq, then Gemini, then local."""
    
    # Try high-speed provider
    report = _evaluate_via_groq(code, task, lang)
    if report: return report

    # Try fallback provider
    report = _evaluate_via_gemini(code, task, lang)
    if report: return report

    # Safe local fallback
    return calculate_heuristic_grade(code, task)
