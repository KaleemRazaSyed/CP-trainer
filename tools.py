from operator import index
import random
import requests

def recommend_problem(topic, score):
    if score < 45:
        return f"{topic} is currently weak. Start with an easy concept-building problem."

    elif score < 70:
        return f"Try a medium {topic} problem with implementation focus."

    else:
        return f"Challenge yourself with a hard {topic} problem."
    
def explain_topic(topic):
    explanations = {
        "dp": "DP solves overlapping subproblems by storing results.",
        "graphs": "Graphs contain nodes and edges. Common techniques include BFS and DFS.",
        "geometry": "Focus on distances, angles, and coordinate relationships."
    }
    return explanations.get(topic, "No explanation available.")

def review_progress(topic, score):
    return f"Your current level in {topic} is {score}/100. Focus on weak patterns and practice consistency."

def make_study_plan(topic, score):
    if score < 45:
        return (
            f"Today: revise core {topic} concept, "
            f"solve 1 easy problem, "
            f"review mistakes at night."
        )

    return (
        f"Today: learn advanced {topic} concept, "
        f"solve 2 medium problems, "
        f"review mistakes at night."
    )

def fetch_codeforces_problems():
    url = f"https://codeforces.com/api/problemset.problems"
    response = requests.get(url)
    data = response.json()

    if data["status"] != "OK":
        return []

    return data["result"]["problems"]

def get_target_band(cf_rating, topic_score):
    adjustment = 0

    if topic_score < 45:
        adjustment = -300
    elif topic_score > 75:
        adjustment = 100

    target = cf_rating + adjustment

    return max(800, target - 100), min(target + 100, 3500)

def filter_problems(problems, topic, target_low, target_high, recommended, solved):
    TOPIC_TAGS = {
    "dp": ["dp"],
    "graphs": ["graphs", "dfs and similar", "trees"],
    "math": ["math", "number theory"]
    }
    
    valid_tags = TOPIC_TAGS.get(topic, [topic])

    problems = [p for p in problems
                if "rating" in p
                and target_low <= p["rating"] <= target_high
                and any(tag in p.get("tags", []) for tag in valid_tags)
                and f'{p["contestId"]}{p["index"]}' not in recommended
                and f'{p["contestId"]}{p["index"]}' not in solved]
    return problems


def recommend_cf_problem(topic, score, memory):

    problems = fetch_codeforces_problems()
    
    if not problems:
        return "No problems found."
    
    recommended = set(memory.get("recommended_problems", []))
    solved = set(memory.get("solved_problems", []))

    target_low, target_high = get_target_band(fetch_user_rating(memory.get("handle", "")), score)

    filtered = filter_problems(problems, topic, target_low, target_high, recommended, solved)

    if not filtered:
        return "No problems found in the desired difficulty range."
    
    selected = random.choice(filtered)

    
    problem_id = f'{selected["contestId"]}{selected["index"]}'
    memory["recommended_problems"].append(problem_id)

    from memory import save_memory
    save_memory(memory)

    return (
        f'{selected["name"]} '
        f'({selected["contestId"]}{selected["index"]}) '
        f'Rating: {selected["rating"]}'
    )

def fetch_user_solved_problems(handle):

    url = f"https://codeforces.com/api/user.status?handle={handle}"

    response = requests.get(url)
    data = response.json()

    if data["status"] != "OK":
        return []

    solved = set()
    for submission in data["result"]:
        if submission["verdict"] == "OK":
            problem = submission["problem"]
        contest_id = problem.get("contestId")
        index = problem.get("index")

        if contest_id is None or index is None:
            continue

        problem_id = f"{contest_id}{index}"
        solved.add(problem_id)
    
    return list(solved)

def fetch_user_rating(handle):
    url = f"https://codeforces.com/api/user.rating?handle={handle}"

    response = requests.get(url)
    data = response.json()

    if data["status"] != "OK" or not data["result"]:
        return 0

    latest = data["result"][-1]

    return latest["newRating"]

