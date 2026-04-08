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
The `TutorAction` model supports high-level tutoring interactions:

| Type | Description | Required Fields |
| :--- | :--- | :--- |
| `suggest_problem` | Skip to a new task | `difficulty` / `topic` |
| `evaluate_code` | Submit code for grading | `code_string`, `language` |
| `adjust_difficulty` | Manually nudge the tutor | `adjustment` ("up" / "down") |

## 👁 Observation Space
The `TutorObservation` provides rich state information after each step:

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
- [x] **Containerized**: `Dockerfile` optimized for HF Spaces (non-root UID 1000).

### Problem Description
Students submit code solutions to Data Structures & Algorithms problems. The engine grades submissions, provides feedback, and dynamically adjusts difficulty based on performance — creating a personalized learning path.

### Real-World Motivation
Traditional DSA learning platforms offer static difficulty. This environment uses RL principles to adaptively match problem difficulty to student capability, creating an optimal learning curve. The agent learns when to advance, when to consolidate, and how to provide targeted feedback.

## 2. Technical Details

### Action Space (`TutorAction`)
| Field | Type | Description |
|---|---|---|
| `action_type` | str | `suggest_problem` \| `evaluate_code` \| `adjust_difficulty` |
| `code_string` | str | Student's code solution |
| `language` | str | `python` \| `cpp` \| `java` \| `javascript` |
| `difficulty` | int | 0 (Easy), 1 (Medium), 2 (Hard) |
| `adjustment` | str | `up` \| `down` |

### Observation Space (`TutorObservation`)
| Field | Type | Description |
|---|---|---|
| `current_problem` | str | Title of the current problem |
| `difficulty` | int | Current difficulty level |
| `feedback_summary` | str | AI feedback on submission |
| `score` | float | Submission correctness (0.0–1.0) |
| `done` | bool | Episode termination flag |
| `reward` | float | Reward signal from last action |

### Session Data (`SessionRecord`)
| Field | Type | Description |
|---|---|---|
| `user_level` | int | Student's current level (0–2) |
| `success_rate` | float | EMA of submission scores |
| `streak` | int | Consecutive good submissions |
| `attempts_count` | int | Total submissions |
| `historical_scores` | list | All submission scores |

## 3. Tasks

### Task 1 — Two Sum (Easy)
Find two indices whose values sum to a target.
- **Grader**: Deterministic (6 test cases)
- **Expected Complexity**: O(N)

### Task 2 — Longest Increasing Subsequence (Medium)
Find the length of the longest strictly increasing subsequence.
- **Grader**: Deterministic (6 test cases)
- **Expected Complexity**: O(N log N)

### Task 3 — Number of Islands (Hard)
Count connected components in a 2D grid.
- **Grader**: Deterministic (6 test cases)
- **Expected Complexity**: O(M×N)

### Task 4 — Valid Parentheses (Easy)
Validate bracket closing order using a stack.
- **Grader**: Deterministic (9 test cases)

### Task 5 — Merge K Sorted Lists (Hard)
Merge multiple sorted lists into one.
- **Grader**: Deterministic (6 test cases)
- **Expected Complexity**: O(N log K)

## 4. Reward Function

| Score Range | Meaning | Reward |
|---|---|---|
| 0.0 – 0.5 | Incorrect / Buggy | 0.0 – 0.40 |
| 0.5 – 0.8 | Correct, Suboptimal | 0.50 – 0.79 |
| 0.8 – 0.9 | High Quality | 0.80 – 0.89 |
| 0.9 – 1.0 | Perfect / Mastered | 0.90 – 1.00 |

**Bonus Signals**:
- **Progress Bonus**: +0.1 for surpassing previous max score.
- **Stagnation Penalty**: -0.05 for submitting identical code.

## 5. Setup Instructions

### Local Run
```bash
pip install -r requirements.txt
export GROQ_API_KEY="your_key"
uvicorn server.app:app --host 0.0.0.0 --port 7860
```
Access the UI at `http://127.0.0.1:7860`

### Running Evaluation
```bash
export MODEL_NAME="llama-3.3-70b-versatile"
export HF_TOKEN="your_hf_token"
python3 inference.py
```

## 6. Architecture

```
DSATutor/
├── server/
│   ├── app.py                  # API Server & Endpoints
│   ├── env.py                  # TutorEngine Logic
│   ├── models.py               # Humanized Data Models
│   ├── tasks.py                # Problem Bank (50+ Tasks)
│   ├── grader.py               # Evaluation Bridge
│   ├── gemini_client.py        # Multi-provider AI (Groq/Gemini)
│   └── deterministic_grader.py # Test Harnesses
├── frontend/                   # Dashboard UI
├── inference.py                # Baseline Agent
├── openenv.yaml                # Environment Spec
└── Dockerfile                  # Production Image
```
