# DSATutor Benchmark

An adaptive reinforcement learning environment for Data Structures and Algorithms tutoring. Built with OpenEnv compliance and socratic feedback logic.

## Project Structure

- `server/`: Core tutoring engine and API logic.
  - `app.py`: FastAPI entry point with OpenEnv endpoints.
  - `env.py`: Reinforcement learning environment logic.
  - `grader.py`: Code evaluation and feedback orchestration.
  - `gemini_client.py`: Multi-provider LLM integration.
  - `deterministic_grader.py`: Test-harness based grading system.
  - `tasks.py`: Standard problem bank.
- `inference.py`: Baseline agent for benchmarking.
- `Dockerfile`: Production-ready container configuration.

## Environment Variables

- `GROQ_API_KEY`: Required for Llama 3 generation/grading.
- `GEMINI_API_KEY`: Required for fallback grading.
- `MODEL_NAME`: Default model (e.g., `llama-3.3-70b-versatile`).
- `PORT`: Server port (default: 7860).

## Quick Start

```bash
# Start the tutor server
python -m server.app

# Run the baseline evaluation
python inference.py
```
