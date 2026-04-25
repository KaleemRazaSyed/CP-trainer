from memory import *
from tools import *
from state import *
from diagnose import *
from policy import *
from execute import *

# from openai import OpenAI

#client = OpenAI()

def fallback_reason(score):
    if score < 40:
        return "easy"
    elif score < 70:
        return "medium"
    return "hard"


def llm_reason(user_input):
    text = user_input.lower()

    scores = {
        "explain": 0,
        "plan": 0,
        "review": 0,
        "problem": 0
    }

    if any(word in text for word in ["explain", "understand", "teach", "concept"]):
        scores["explain"] += 2

    if any(word in text for word in ["plan", "study", "schedule", "today", "prepare"]):
        scores["plan"] += 2

    if any(word in text for word in ["review", "progress", "weak", "mistakes"]):
        scores["review"] += 2

    if any(word in text for word in ["problem", "question", "practice", "solve"]):
        scores["problem"] += 2

    return max(scores, key=scores.get)


def run_agent():
    problem_id = input("Problem ID: ")
    solved = input("Solved? (yes/no): ").lower() == "yes"
    solve_time = int(input("Solve time (minutes): "))
    used_editorial = input("Used editorial? (yes/no): ").lower() == "yes"

    state = build_state(
        problem_id,
        solved,
        solve_time,
        used_editorial
    )

    diagnosis = diagnose(state)

    decision = decide_next_action(diagnosis)

    print("\nState:")
    print(state)

    print("\nDiagnosis:")
    print(diagnosis)

    print("\nDecision:")
    print(decision)
    memory = load_memory()

    topic = input("Topic: ")
    current_rating = int(input("Current target rating: "))

    recommendation = execute_action(
        decision,
        topic,
        memory,
        current_rating
    )

    print("\nRecommended Next Problem:")
    print(recommendation)