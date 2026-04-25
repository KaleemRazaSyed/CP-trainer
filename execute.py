from tools import recommend_cf_problem


def execute_action(decision, topic, memory):
    topic_score = memory["topic_scores"].get(topic, 50)

    return recommend_cf_problem(
        topic,
        topic_score,
        memory
    )