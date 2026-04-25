def build_state(problem_id, solved, solve_time, used_editorial):
    return {
        "problem_id": problem_id,
        "solved": solved,
        "solve_time": solve_time,
        "used_editorial": used_editorial
    }