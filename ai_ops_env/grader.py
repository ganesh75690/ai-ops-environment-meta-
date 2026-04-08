def grade_easy(action, task):
    if task.priority == "high" and action.action_type == "assign":
        return 0.99  # Force below 1.0
    elif action.action_type == "assign":
        return 0.5
    return 0.01  # Force above 0.0


def grade_medium(action, task):
    score = 0.0

    if task.priority == "high" and action.action_type == "assign":
        score += 0.6
    if task.priority == "medium" and action.action_type == "assign":
        score += 0.3
    if action.action_type == "escalate":
        score += 0.2

    return min(score, 1.0)


def grade_hard(actions, tasks):
    score = 0.0

    for action in actions:
        task = next((t for t in tasks if t.id == action.task_id), None)
        if not task:
            continue

        if task.priority == "high" and action.action_type == "assign":
            score += 0.4
        elif task.priority == "medium" and action.action_type == "assign":
            score += 0.2
        elif action.action_type == "ignore":
            score -= 0.3

    return max(0.0, min(score, 1.0))
