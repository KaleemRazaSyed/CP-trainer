import json

MEMORY_FILE = "data/memory.json"

def load_memory():
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


def update_topic_score(memory, topic, delta):
    memory["topic_scores"][topic] = max(
        0,
        min(100, memory["topic_scores"].get(topic, 50) + delta)
    )
    save_memory(memory)

def update_solved_problems(memory, solved_list):
    memory["solved_problems"] = solved_list
    save_memory(memory)