"""
Deterministic Grading Suite.
Executes student code against pre-defined test harnesses to ensure 
reproducibility and precise scoring for core DSA tasks.
"""

import sys
import io
import traceback
from contextlib import redirect_stdout, redirect_stderr

def run_test_harness(code: str, test_script: str) -> dict:
    """
    Executes student code within a controlled namespace and runs the 
    corresponding test script. Captures passes, totals, and errors.
    """
    passed = 0
    total = 0
    errors = []

    # Inject the test script after the student's submission
    execution_payload = code + "\n\n" + test_script

    try:
        # Buffer streams for output capture
        stdout_buf = io.StringIO()
        stderr_buf = io.StringIO()

        import heapq, copy, collections, math
        # Provide common utilities for DSA implementations
        shared_namespace = {
            "__builtins__": __builtins__,
            "heapq": heapq,
            "copy": copy,
            "collections": collections,
            "math": math,
        }

        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            exec(execution_payload, shared_namespace)

        # Retrieve results assigned by the test script
        passed = shared_namespace.get("_passed", 0)
        total = shared_namespace.get("_total", 0)

    except SyntaxError as se:
        errors.append(f"Syntax error in submission: {se}")
    except NameError as ne:
        errors.append(f"Referenced unknown variable: {ne}")
    except Exception as exc:
        errors.append(f"Runtime error: {type(exc).__name__} - {exc}")

    return {"passed": passed, "total": total, "errors": errors}

# --- Task 1: Two Sum (Easy) ---

TASK1_HARNESS = """
_passed = 0
_total = 0
_cases = [
    ([2, 7, 11, 15], 9, {0, 1}),
    ([3, 2, 4], 6, {1, 2}),
    ([3, 3], 6, {0, 1}),
    ([1, 5, 3, 7, 2], 9, {3, 4}),
    ([-1, -2, -3, -4, -5], -8, {2, 4}),
    ([0, 4, 3, 0], 0, {0, 3}),
]
for nums, target, expected in _cases:
    _total += 1
    try:
        res = two_sum(nums, target)
        if res is not None and set(res) == expected:
            _passed += 1
    except Exception:
        pass
"""

TASK1_METADATA = {
    "id": "task_two_sum",
    "title": "Two Sum",
    "topic": "Arrays",
    "difficulty": 0,
    "description": "Find indices of two numbers adding up to target in O(N) time. Define `two_sum(nums, target)`.",
}

# --- Task 2: Longest Increasing Subsequence (Medium) ---

TASK2_HARNESS = """
_passed = 0
_total = 0
_cases = [
    ([10, 9, 2, 5, 3, 7, 101, 18], 4),
    ([0, 1, 0, 3, 2, 3], 4),
    ([7, 7, 7, 7, 7, 7, 7], 1),
    ([1, 2, 3, 4, 5], 5),
    ([5, 4, 3, 2, 1], 1),
    ([3, 10, 2, 1, 20], 3),
]
for nums, expected in _cases:
    _total += 1
    try:
        if lis_length(nums) == expected:
            _passed += 1
    except Exception:
        pass
"""

TASK2_METADATA = {
    "id": "task_lis",
    "title": "Longest Increasing Subsequence",
    "topic": "Dynamic Programming",
    "difficulty": 1,
    "description": "Return the length of the longest strictly increasing subsequence in O(N log N). Define `lis_length(nums)`.",
}

# --- Task 3: Number of Islands (Hard) ---

TASK3_HARNESS = """
_passed = 0
_total = 0
import copy
_cases = [
    ([["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]], 1),
    ([["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]], 3),
    ([["0","0","0"],["0","0","0"]], 0),
    ([["1"]], 1),
    ([["1","0","1","0","1"],["0","1","0","1","0"],["1","0","1","0","1"]], 8),
    ([["1","1","1"],["0","1","0"],["1","1","1"]], 1),
]
for grid, expected in _cases:
    _total += 1
    try:
        if num_islands(copy.deepcopy(grid)) == expected:
            _passed += 1
    except Exception:
        pass
"""

TASK3_METADATA = {
    "id": "task_islands",
    "title": "Number of Islands",
    "topic": "Graphs",
    "difficulty": 2,
    "description": "Count islands in a 2D water/land grid. Define `num_islands(grid)`.",
}

# --- Task 4: Valid Parentheses (Easy) ---

TASK4_HARNESS = """
_passed = 0
_total = 0
_cases = [
    ("()", True), ("()[]{}", True), ("(]", False), ("([)]", False),
    ("{[]}", True), ("((()))", True), ("", True), ("(", False), ("())", False),
]
for s, expected in _cases:
    _total += 1
    try:
        if is_valid(s) == expected:
            _passed += 1
    except Exception:
        pass
"""

TASK4_METADATA = {
    "id": "task_valid_parentheses",
    "title": "Valid Parentheses",
    "topic": "Stacks & Queues",
    "difficulty": 0,
    "description": "Determine if string of brackets is valid in O(N). Define `is_valid(s)`.",
}

# --- Task 5: Merge K Sorted Lists (Hard) ---

TASK5_HARNESS = """
_passed = 0
_total = 0
import heapq
_cases = [
    ([[1,4,5],[1,3,4],[2,6]], [1,1,2,3,4,4,5,6]),
    ([], []), ([[]], []), ([[1]], [1]),
    ([[1,2],[1,2]], [1,1,2,2]),
    ([[10,20,30],[5,15,25],[0,50,100]], [0,5,10,15,20,25,30,50,100]),
]
for lists, expected in _cases:
    _total += 1
    try:
        if merge_k_lists(lists) == expected:
            _passed += 1
    except Exception:
        pass
"""

TASK5_METADATA = {
    "id": "task_merge_k_lists",
    "title": "Merge K Sorted Lists",
    "topic": "Linked Lists",
    "difficulty": 2,
    "description": "Merge k sorted lists into a single sorted Python list. Define `merge_k_lists(lists)`.",
}

# Registry for evaluation
FIXED_TASKS = [
    {"info": TASK1_METADATA, "tests": TASK1_HARNESS},
    {"info": TASK2_METADATA, "tests": TASK2_HARNESS},
    {"info": TASK3_METADATA, "tests": TASK3_HARNESS},
    {"info": TASK4_METADATA, "tests": TASK4_HARNESS},
    {"info": TASK5_METADATA, "tests": TASK5_HARNESS},
]

def grade_deterministic(code: str, task_id: str) -> dict:
    """
    Primary interface for deterministic grading.
    Finds the benchmark by ID, executes the harness, and returns formatted feedback.
    """
    active_task = next((t for t in FIXED_TASKS if t["info"]["id"] == task_id), None)

    if not active_task:
        return {
            "correctness": 0.0, "passed": 0, "total": 0,
            "feedback": f"Grade harness not found for ID: {task_id}", "errors": [],
        }

    results = run_test_harness(code, active_task["tests"])
    passing = results["passed"]
    total = results["total"]
    failures = results["errors"]

    score = round(passing / total, 2) if total > 0 else 0.0

    # Local debugging log (internal)
    import logging
    debug_log = logging.getLogger(__name__)

    if failures:
        debug_log.error(f"Grader failed on {task_id}: {failures}")
        feedback = f"It looks like there's a runtime issue: {failures[0]}"
    elif score >= 0.9:
        feedback = f"Perfect! You've passed all {passing} test cases."
    elif score >= 0.5:
        feedback = f"Not bad. You passed {passing}/{total} cases, but missed some edge conditions."
    else:
        feedback = f"Only {passing}/{total} cases passed. Try walking through your logic again."

    return {
        "correctness": score,
        "passed": passing,
        "total": total,
        "feedback": feedback,
        "errors": failures,
    }
