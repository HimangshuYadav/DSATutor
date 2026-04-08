import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from typing import Dict, Any

# Task Definitions and Standard Metadata

TASK1_METADATA = {
    "id": "task1",
    "title": "Two Sum",
    "difficulty": "Easy",
    "topic": "Arrays"
}
TASK1_HARNESS = """
_passed = 0
_total = 0
_cases = [([2,7,11,15], 9, {0,1}), ([3,2,4], 6, {1,2}), ([3,3], 6, {0,1})]
for nums, target, expected in _cases:
    _total += 1
    try:
        res = two_sum(nums, target)
        if res is not None and set(res) == expected:
            _passed += 1
    except: pass
"""

TASK2_METADATA = {
    "id": "task2",
    "title": "Longest Increasing Subsequence",
    "difficulty": "Medium",
    "topic": "DP"
}
TASK2_HARNESS = """
_passed = 0
_total = 0
_cases = [([10,9,2,5,3,7,101,18], 4), ([0,1,0,3,2,3], 4), ([7,7,7,7,7], 1)]
for nums, expected in _cases:
    _total += 1
    try:
        if lis_length(nums) == expected: _passed += 1
    except: pass
"""

TASK3_METADATA = {
    "id": "task3",
    "title": "Number of Islands",
    "difficulty": "Hard",
    "topic": "Graphs"
}
TASK3_HARNESS = """
_passed = 0
_total = 0
_cases = [
    ([["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"]], 2),
    ([["1"]], 1),
    ([["0"]], 0)
]
for grid, expected in _cases:
    _total += 1
    try:
        if num_islands(grid) == expected: _passed += 1
    except: pass
"""

TASK4_METADATA = {
    "id": "task4",
    "title": "Valid Parentheses",
    "difficulty": "Easy",
    "topic": "Stacks"
}
TASK4_HARNESS = """
_passed = 0
_total = 0
_cases = [("()", True), ("()[]{}", True), ("(]", False), ("([)]", False)]
for s, expected in _cases:
    _total += 1
    try:
        if is_valid(s) == expected: _passed += 1
    except: pass
"""

TASK5_METADATA = {
    "id": "task5",
    "title": "Merge K Sorted Lists",
    "difficulty": "Hard",
    "topic": "Heaps"
}
TASK5_HARNESS = """
_passed = 0
_total = 0
_cases = [([[1,4,5],[1,3,4],[2,6]], [1,1,2,3,4,4,5,6]), ([], []), ([[1]], [1])]
for lists, expected in _cases:
    _total += 1
    try:
        if merge_k_lists(lists) == expected: _passed += 1
    except: pass
"""

FIXED_TASKS = [
    {"info": TASK1_METADATA, "tests": TASK1_HARNESS},
    {"info": TASK2_METADATA, "tests": TASK2_HARNESS},
    {"info": TASK3_METADATA, "tests": TASK3_HARNESS},
    {"info": TASK4_METADATA, "tests": TASK4_HARNESS},
    {"info": TASK5_METADATA, "tests": TASK5_HARNESS},
]

def grade_deterministic(code: str, task_id: str) -> Dict[str, Any]:
    """Runs a code submission against a fixed test harness."""
    active_task = next((t for t in FIXED_TASKS if t["info"]["id"] == task_id), None)
    if not active_task:
        return {"score": 0.0, "passed": 0, "total": 0, "feedback": "Problem configuration missing."}
    
    results = run_test_harness(code, active_task["tests"])
    passed = results["passed"]
    total = results["total"]
    
    score = round(passed / total, 2) if total > 0 else 0.0
    
    feedback = f"Great work! You passed all {total} test cases." if score >= 1.0 else f"Only {passed}/{total} cases passed. Review your edge cases."
    if results["errors"]:
        feedback = f"Your code encountered a runtime error: {results['errors'][0]}"
        
    return {
        "score": score,
        "passed": passed,
        "total": total,
        "feedback": feedback,
        "traceback": results["errors"]
    }

def run_test_harness(code: str, test_script: str) -> Dict[str, Any]:
    """Safely executes student code within a test harness."""
    stdout_buf = io.StringIO()
    stderr_buf = io.StringIO()
    passed, total = 0, 0
    errors = []
    
    try:
        import heapq, copy, collections, math, typing
        shared_namespace = {
            "__builtins__": __builtins__,
            "heapq": heapq,
            "copy": copy,
            "collections": collections,
            "math": math,
            "typing": typing
        }
        execution_payload = f"{code}\n\n{test_script}"
        
        with redirect_stdout(stdout_buf), redirect_stderr(stderr_buf):
            exec(execution_payload, shared_namespace)
            
        passed = shared_namespace.get("_passed", 0)
        total = shared_namespace.get("_total", 0)
    except Exception as exc:
        errors.append(f"Runtime error: {type(exc).__name__} - {exc}")
        
    return {"passed": passed, "total": total, "errors": errors}
