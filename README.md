---
title: DSATutor
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
tags:
- openenv
---

# DSATutor — OpenEnv RL Environment

An **adaptive, AI-powered DSA tutoring** environment built on the [OpenEnv](https://github.com/meta-pytorch/OpenEnv) specification.

## 🚀 Motivation
The **DSATutor** environment models a high-stakes real-world task: technical interview preparation. Unlike standard "pass/fail" coding environments, it uses a **Socratic feedback loop** powered by LLMs to provide dense training signals. Agents are evaluated not just on their ability to solve a problem, but on their ability to **improve iteratively** based on hints.

## 🛠 Action Space
The `DSAAction` model supports high-level tutoring interactions:

| Type | Description | Required Fields |
| :--- | :--- | :--- |
| `suggest_problem` | Skip to a new task | `difficulty` / `topic` |
| `evaluate_code` | Submit code for grading | `code_string`, `language` |
| `adjust_difficulty` | Manually nudge the tutor | `adjustment` ("up" / "down") |

## 👁 Observation Space
The `DSAObservation` provides rich state information after each step:

| Field | Type | Description |
| :--- | :--- | :--- |
| `current_problem` | `str` | Title of the active DSA task |
| `score` | `float` | Correctness (0.0 to 1.0) of last submission |
| `feedback_summary` | `str` | Socratic hints and error analysis |
| `reward` | `float` | Dense reward (correctness + improvement bonus) |

## 📊 Verified Baseline Scores
Tested using `llama-3.3-70b-versatile` over 5 deterministic episodes.

| Task | Topic | Difficulty | Success | Score (Mean) |
| :--- | :--- | :--- | :--- | :--- |
| **Two Sum** | Arrays | Easy | 100% | 1.000 |
| **Valid Parentheses** | Stacks | Easy | 100% | 1.000 |
| **LIS** | DP | Medium | 100% | 1.000 |
| **Number of Islands** | Graphs | Hard | 100% | 1.000 |
| **Merge K Lists** | Linked Lists| Hard | 100% | 1.000 |

## 🏁 Final Compliance Status
- [x] **OpenEnv spec compliance**: 100% pass on `openenv validate`.
- [x] **3+ tasks with graders**: 5 deterministic tasks verified.
- [x] **Meaningful reward**: Includes incremental progress rewards (+0.1) and stagnation penalties (-0.05).
- [x] **Baseline Reproducible**: `inference.py` follows strict async/STDOUT spec.
- [x] **Containerized**: `Dockerfile` ready with non-root UID 1000 user.

### Problem Description
Students submit code solutions to Data Structures & Algorithms problems. The environment grades submissions, provides feedback, and dynamically adjusts difficulty based on performance — creating a personalized learning path.

### Real-World Motivation
Traditional DSA learning platforms offer static difficulty. This environment uses RL principles to adaptively match problem difficulty to student capability, creating an optimal learning curve. The agent learns when to advance, when to consolidate, and how to provide targeted feedback.

## 2. Technical Details

### Action Space (`DSAAction`)
| Field | Type | Description |
|---|---|---|
| `action_type` | str | `suggest_problem` \| `evaluate_code` \| `adjust_difficulty` |
| `code_string` | str | Student's code solution |
| `language` | str | `python` \| `cpp` \| `java` \| `javascript` |
| `difficulty` | int | 0 (Easy), 1 (Medium), 2 (Hard) |
| `adjustment` | str | `up` \| `down` |

### Observation Space (`DSAObservation`)
| Field | Type | Description |
|---|---|---|
| `current_problem` | str | Title of the current problem |
| `difficulty` | int | Current difficulty level |
| `feedback_summary` | str | AI feedback on submission |
| `score` | float | Submission correctness (0.0–1.0) |
| `done` | bool | Episode termination flag |
| `reward` | float | Reward signal from last action |

### State (`EnvState`)
| Field | Type | Description |
|---|---|---|
| `user_level` | int | Student's current level (0–2) |
| `success_rate` | float | EMA of submission scores |
| `streak` | int | Consecutive good submissions |
| `attempts_count` | int | Total submissions |
| `historical_scores` | list | All submission scores |

## 3. Tasks

### Task 1 — Two Sum (Easy)
Find two indices whose values sum to a target. Tests hash map usage and O(N) thinking.
- **Grader**: Deterministic (6 test cases)
- **Expected Complexity**: O(N)

### Task 2 — Longest Increasing Subsequence (Medium)
Find the length of the longest strictly increasing subsequence. Tests dynamic programming.
- **Grader**: Deterministic (6 test cases)
- **Expected Complexity**: O(N log N)

### Task 3 — Number of Islands (Hard)
Count connected components in a 2D grid. Tests graph traversal (BFS/DFS).
- **Grader**: Deterministic (6 test cases)
- **Expected Complexity**: O(M×N)

### Task 4 — Valid Parentheses (Easy)
Validate bracket closing order using a stack.
- **Grader**: Deterministic (9 test cases)
- **Expected Complexity**: O(N)

### Task 5 — Merge K Sorted Lists (Hard)
Merge multiple sorted lists into one. Tests heap usage and efficiency.
- **Grader**: Deterministic (6 test cases)
- **Expected Complexity**: O(N log K)

### Bonus: 50+ Additional Problems
The environment includes 50+ diverse problems across 9 topics (Arrays, Strings, Trees, Graphs, DP, etc.) graded by AI for the interactive web UI.

## 4. Reward Function

| Score Range | Meaning | Reward |
|---|---|---|
| 0.0 – 0.3 | Wrong / crashes | 0.0 – 0.24 |
| 0.3 – 0.5 | Partially correct | 0.24 – 0.39 |
| 0.5 – 0.8 | Correct, suboptimal | 0.50 – 0.79 |
| 0.8 – 0.9 | Correct & efficient | 0.80 – 0.89 |
| 0.9 – 1.0 | Perfect | 0.90 – 1.00 |

**Penalties**: Skipping a problem: -0.1, level decrease  
**Completion**: Level 2 + success_rate ≥ 0.8 + 5 attempts + streak ≥ 3

## 5. Setup Instructions

### Local (without Docker)
```bash
pip install -r requirements.txt
export GROQ_API_KEY="your_groq_key"
uv run server
```
Access at `http://127.0.0.1:7860`

### Running Inference
```bash
export API_BASE_URL="http://127.0.0.1:7860"
export MODEL_NAME="llama-3.3-70b-versatile"
export HF_TOKEN="your_hf_token"
python3 inference.py
```

## 6. Docker Usage
```bash
docker build -t dsatutor-env .
docker run -p 7860:7860 \
  -e GROQ_API_KEY="your_key" \
  dsatutor-env
```

## 7. HF Deployment
1. Create a new Space on huggingface.co/spaces (Docker SDK)
2. Push these files to the repository
3. Set Secrets: `GROQ_API_KEY`, `GEMINI_API_KEY`
4. The `/reset`, `/step`, `/state` endpoints validate OpenEnv compliance

## 8. Environment Configuration Variables
| Variable | Required | Description |
|---|---|---|
| `API_BASE_URL` | Yes | Base URL of the environment server |
| `MODEL_NAME` | Yes | LLM model name for inference |
| `HF_TOKEN` | Optional | Hugging Face token |
| `GROQ_API_KEY` | Yes | Groq API key for AI grading |
| `GEMINI_API_KEY` | Optional | Gemini API key (fallback grading) |

## 9. Baseline Results
Using `llama-3.3-70b-versatile` across all 5 deterministic tasks:

| Task | Difficulty | Score | Status |
|---|---|---|---|
| Two Sum | Easy | 1.000 | ✅ |
| Valid Parentheses | Easy | 1.000 | ✅ |
| LIS | Medium | 1.000 | ✅ |
| Number of Islands | Hard | 1.000 | ✅ |
| Merge K Lists | Hard | 1.000 | ✅ |

## 10. Architecture
```
DSATutor/
├── server/
│   ├── app.py                  # FastAPI + OpenEnv endpoints
│   ├── env.py                  # Environment (subclasses openenv.Environment)
│   ├── models.py               # Typed models (OpenEnv Action/Observation)
│   ├── tasks.py                # Static problem bank
│   ├── grader.py               # AI-powered grading (Groq)
│   ├── gemini_client.py        # Multi-provider AI client
│   └── deterministic_grader.py # Test-case graders for fixed tasks
├── frontend/
│   ├── index.html              # Web UI
│   ├── script.js               # Frontend logic
│   └── style.css               # Styling
├── inference.py                # Baseline inference script
├── openenv.yaml                # OpenEnv configuration
├── Dockerfile                  # Container deployment
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```
