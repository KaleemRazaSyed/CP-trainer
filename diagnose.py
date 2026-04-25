def diagnose(state):
    if not state["solved"]:
        return {
            "mode": "warmup",
            "performance": "weak"
        }

    if state["used_editorial"]:
        return {
            "mode": "bridge",
            "performance": "partial"
        }

    if state["solve_time"] <= 30:
        return {
            "mode": "stretch",
            "performance": "strong"
        }

    return {
        "mode": "normal",
        "performance": "good"
    }