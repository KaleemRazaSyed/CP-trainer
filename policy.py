def decide_next_action(diagnosis):
    mode = diagnosis["mode"]

    if mode == "warmup":
        return {
            "difficulty_shift": -200,
            "action": "recommend_easy_problem"
        }

    if mode == "bridge":
        return {
            "difficulty_shift": -100,
            "action": "recommend_bridge_problem"
        }

    if mode == "stretch":
        return {
            "difficulty_shift": 100,
            "action": "recommend_stretch_problem"
        }

    return {
        "difficulty_shift": 0,
        "action": "recommend_normal_problem"
    }