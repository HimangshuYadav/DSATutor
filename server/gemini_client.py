import os
import json
import re
import logging
from openai import OpenAI
from google import genai

# Logging configuration
logger = logging.getLogger(__name__)

# Provider configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

# Initialize OpenAI-compatible client for Groq or similar providers
client = OpenAI(
    base_url=os.getenv("API_BASE_URL", "https://api.groq.com/openai/v1"),
    api_key=GROQ_API_KEY or GEMINI_API_KEY # Some users use Gemini keys through a proxy
)

def evaluate_with_ai(code: str, task: dict, language: str) -> dict:
    """Performs deep code evaluation using available AI providers."""
    try:
        # Standardize interaction with LLM
        system_prompt = (
            "You are a specialized DSA Tutor. Evaluate the submission's CORRECTNESS (0-1) "
            "and provide SOCRATIC FEEDBACK in valid JSON format. "
            "The JSON must have these keys: 'correctness' (float), 'feedback' (string), "
            "'strengths' (list of strings), 'weaknesses' (list of strings), 'suggestions' (list of strings)."
        )
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Problem: {task['prompt']}\nLanguage: {language}\nSubmitted Code:\n{code}"}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        logger.warning(f"Primary AI evaluation failed: {e}. Falling back to Gemini SDK.")
        if GEMINI_API_KEY:
            return _evaluate_via_gemini_sdk(code, task, language)
        return {"correctness": calculate_heuristic_grade(code, task), "feedback": "Evaluation completed via local reasoning engine."}

def _evaluate_via_gemini_sdk(code: str, task: dict, lang: str) -> dict:
    """Direct fallback to Google GenAI SDK if OpenAI-style proxy fails."""
    try:
        engine = genai.Client(api_key=GEMINI_API_KEY)
        response = engine.models.generate_content(
            model="gemini-2.0-flash",
            contents=f"Extract JSON evaluation {{'correctness': float, 'feedback': str}} for:\nProblem: {task['prompt']}\nCode: {code}"
        )
        match = re.search(r"\{.*\}", response.text, re.DOTALL)
        return json.loads(match.group())
    except Exception as inner:
        logger.error(f"Gemini SDK fallback also failed: {inner}")
        return {"correctness": 0.0, "feedback": "Critical evaluation error. Please ensure your API keys are valid."}

def calculate_heuristic_grade(code: str, task: dict) -> float:
    """Purely local heuristic for grading when all AI providers are unreachable."""
    # Basic logic check
    score = 0.0
    if "def " in code: score += 0.2
    if "return " in code: score += 0.2
    if any(keyword in code for keyword in ["for", "while"]): score += 0.2
    return min(score, 1.0)
