class Evaluator:
    """
    Evaluates agent performance across multiple tasks.

    This module is designed to simulate benchmarking of
    decision-making strategies in the environment.
    """

    def evaluate(self, rewards):
        """
        Compute average reward.

        Args:
            rewards (list): List of reward values

        Returns:
            float: Average score
        """
        if not rewards:
            return 0.0
        return sum(rewards) / len(rewards)
