def success_rate(rewards):
    """
    Calculate success rate based on positive rewards.

    Args:
        rewards (list): Reward list

    Returns:
        float: Success rate
    """
    if not rewards:
        return 0.0

    success = [r for r in rewards if r > 0]
    return len(success) / len(rewards)


def average_reward(rewards):
    """
    Compute average reward.
    """
    if not rewards:
        return 0.0
    return sum(rewards) / len(rewards)
