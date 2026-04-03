from ai_ops_env.environment import OpsEnv
from ai_ops_env.models import Action
import random
import time

# Learning memory for adaptive behavior
learning_memory = {
    "high": 0,
    "medium": 0,
    "low": 0
}


def bar(value, max_val=5):
    filled = int((value / max_val) * 10)
    return "[" + "#" * filled + "-" * (10 - filled) + "]"


def calculate_score(task):
    score = 0

    if task.priority == "high":
        score += 3
    elif task.priority == "medium":
        score += 2
    else:
        score += 1

    # simulate urgency / load factor
    import random
    score += random.uniform(0, 1)

    return score


# ✅ Learning agent (adapts over time)
def learning_agent(task, system_load):
    score = calculate_score(task)

    # learning boost
    score += learning_memory[task.priority]

    # threshold changes with system load
    threshold = 3.5 if system_load > 75 else 3

    if score >= threshold:
        action = "assign"
    else:
        action = "ignore"

    return action, score


# ✅ Smart decision engine agent (legacy)
def smart_agent(task, system_load):
    score = calculate_score(task)

    # system under high load → stricter decisions
    if system_load > 75:
        threshold = 3.5
    else:
        threshold = 3

    if score >= threshold:
        return "assign", score
    else:
        return "ignore", score


# ✅ Simple rule-based agent (legacy)
def simple_agent(task):
    if task.priority == "high":
        return "assign"
    elif task.priority == "medium":
        return "assign"
    else:
        return "ignore"


# ✅ Main simulation
def run_baseline():
    env = OpsEnv()
    obs = env.reset()

    total_reward = 0
    steps = 0
    assigned = 0
    ignored = 0
    
    system_load = random.randint(40, 90)  # %
    print(f"\n⚙️ System Load: {system_load}%")

    while steps < 5:   # limit steps
        print(f"\nStep {steps+1}")
        step_reward = 0
        
        print("\n📋 TASK QUEUE STATUS")
        for task in obs.tasks:
            print(f"Task {task.id} | Priority: {task.priority}")
        print("-" * 40)

        for task in obs.tasks:
            print(f"⏳ Processing Task {task.id}...")
            time.sleep(0.3)
            
            action_type, score = learning_agent(task, system_load)

            action = Action(
                task_id=task.id,
                action_type=action_type
            )

            obs, reward, done, _ = env.step(action)
            
            confidence = min(score / 4, 1.0)
            reason = f"Score={score:.2f} → {'High priority decision' if score >= 3 else 'Deferred'}"

            print(f"""
Task {task.id}
  Priority   : {task.priority}
  Decision   : {action_type}
  Score      : {score:.2f}
  Score Visual: {bar(score)}
  Confidence : {confidence:.2f}
  Reason     : {reason}
  Reward     : {reward}
""")
            
            if learning_memory[task.priority] > 0.2:
                print("📈 Agent learned this priority is important")
            
            if task.priority == "high" and action_type == "ignore":
                print("⚠️ ALERT: High priority task ignored!")

            total_reward += reward
            step_reward += reward
            
            # Update learning memory based on reward
            if reward > 0:
                learning_memory[task.priority] += 0.1
            else:
                learning_memory[task.priority] -= 0.05
            
            if action_type == "assign":
                assigned += 1
            else:
                ignored += 1
        print(f"Step {steps+1} Total Reward: {step_reward}")
        print("\n🧠 Learning State:")
        for k, v in learning_memory.items():
            print(f"{k}: {v:.2f}")
        print("-" * 40)
        steps += 1

    print("\n===== 🚀 AI OPS EXECUTIVE REPORT =====")
    print(f"📊 Total Reward: {total_reward}")
    print(f"📈 Avg Reward: {total_reward / steps:.2f}")
    print(f"⚙️ System Load: {system_load}%")
    print(f"✅ Tasks Assigned: {assigned}")
    print(f"⏳ Tasks Ignored: {ignored}")
    print(f"🎯 Efficiency: {(assigned/(assigned+ignored))*100:.2f}%")
    
    if total_reward > 5:
        print("🟢 System Performance: OPTIMAL")
    else:
        print("🟡 System Performance: NEEDS IMPROVEMENT")
    
    print("\n🤖 Agent Evolution Summary:")
    for k, v in learning_memory.items():
        if v > 0:
            print(f"{k}: Improved handling")
        else:
            print(f"{k}: Needs improvement")


# ✅ Entry point
if __name__ == "__main__":
    run_baseline()