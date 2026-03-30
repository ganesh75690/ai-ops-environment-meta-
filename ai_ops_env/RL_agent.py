"""
RL Agent Module for AI Ops Environment

Includes:
- Base agent interface
- Rule-based agent
- Random agent
- Learning agent (pseudo-RL)
- Training & evaluation
- Learning curve visualization
"""

from typing import Dict, Any
import random
import matplotlib.pyplot as plt


# =========================================================
# 🔹 Base Agent
# =========================================================
class BaseAgent:
    def select_action(self, state: Dict[str, Any]) -> str:
        raise NotImplementedError


# =========================================================
# 🔹 Rule-Based Agent
# =========================================================
class RuleBasedAgent(BaseAgent):
    def select_action(self, state: Dict[str, Any]) -> str:
        priority = state.get("priority", "low")

        if priority == "high":
            return "escalate"
        elif priority == "medium":
            return "assign"
        else:
            return random.choice(["assign", "ignore"])


# =========================================================
# 🔹 Random Agent
# =========================================================
class RandomAgent(BaseAgent):
    ACTIONS = ["assign", "escalate", "resolve", "ignore"]

    def select_action(self, state: Dict[str, Any]) -> str:
        return random.choice(self.ACTIONS)


# =========================================================
# 🔹 Learning Agent (Pseudo RL)
# =========================================================
class LearningAgent(BaseAgent):
    ACTIONS = ["assign", "escalate", "resolve", "ignore"]

    def __init__(self, learning_rate: float = 0.1, epsilon: float = 0.2):
        self.q_table = {}
        self.lr = learning_rate
        self.epsilon = epsilon

    def _get_state_key(self, state: Dict[str, Any]) -> str:
        priority = state.get("priority", "low")
        complexity = state.get("complexity", "low")
        return f"{priority}_{complexity}"

    def select_action(self, state: Dict[str, Any]) -> str:
        state_key = self._get_state_key(state)

        # Exploration
        if random.random() < self.epsilon:
            return random.choice(self.ACTIONS)

        # Exploitation
        q_values = {
            action: self.q_table.get((state_key, action), 0.0)
            for action in self.ACTIONS
        }

        return max(q_values, key=q_values.get)

    def update(self, state: Dict[str, Any], action: str, reward: float):
        state_key = self._get_state_key(state)
        current_q = self.q_table.get((state_key, action), 0.0)

        new_q = current_q + self.lr * (reward - current_q)
        self.q_table[(state_key, action)] = new_q


# =========================================================
# 🔹 Run Episode
# =========================================================
def run_episode(env, agent: BaseAgent, train: bool = False) -> float:
    state = env.reset()
    done = False
    total_reward = 0.0

    while not done:
        action = agent.select_action(state)
        next_state, reward, done, _ = env.step(action)

        if train and hasattr(agent, "update"):
            agent.update(state, action, reward)

        state = next_state
        total_reward += reward

    return total_reward


# =========================================================
# 🔹 Train Agent
# =========================================================
def train_agent(env, agent: BaseAgent, episodes: int = 50):
    rewards = []

    for _ in range(episodes):
        reward = run_episode(env, agent, train=True)
        rewards.append(reward)

    return rewards


# =========================================================
# 🔹 Evaluate Agent
# =========================================================
def evaluate_agent(env, agent: BaseAgent, episodes: int = 10) -> float:
    total = 0.0

    for _ in range(episodes):
        total += run_episode(env, agent, train=False)

    return total / episodes


# =========================================================
# 🔹 Plot Learning Curve
# =========================================================
def plot_learning_curve(rewards):
    plt.figure(figsize=(8, 5))
    plt.plot(rewards, marker='o')
    plt.title("Learning Curve (Reward vs Episodes)")
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("learning_curve.png")
    plt.close()


# =========================================================
# 🔹 Main (Local Demo)
# =========================================================
if __name__ == "__main__":
    from ai_ops_env.environment import OpsEnv

    env = OpsEnv()
    agent = LearningAgent()

    print("🔹 Training agent...")
    rewards = train_agent(env, agent, episodes=30)

    print("📈 Generating learning graph...")
    plot_learning_curve(rewards)

    print("🔹 Evaluating agent...")
    score = evaluate_agent(env, agent, episodes=5)

    print(f"Final Average Reward: {score:.2f}")
    print("✅ Graph saved as learning_curve.png")
