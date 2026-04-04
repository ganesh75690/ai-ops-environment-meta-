import random
from ai_ops_env.environment import OpsEnv
from ai_ops_env.models import Action


# -------------------------------
# HEALTH SYSTEM
# -------------------------------
def calculate_system_health(tasks):
    high = sum(1 for t in tasks if t.priority == "high")
    medium = sum(1 for t in tasks if t.priority == "medium")
    low = sum(1 for t in tasks if t.priority == "low")

    total = len(tasks) if tasks else 1

    health = 1 - ((high * 0.6 + medium * 0.3 + low * 0.1) / total)
    return max(0, min(1, health))


# -------------------------------
# ADAPTIVE SMART AGENT (UPGRADED)
# -------------------------------
def smart_agent(task, health_score, performance):
    explore = random.random()
    history = performance[task.priority]
    recent = history[-3:] if len(history) >= 3 else history
    avg_reward = sum(recent) / len(recent) if recent else 0.5

    if task.priority == "high":
        confidence = 0.90 + (avg_reward * 0.1)
        if avg_reward < 0.5:
            return "assign", confidence, "Boost high priority recovery"
        return "assign", confidence, "Critical task"

    elif task.priority == "medium":
        confidence = 0.90 + (avg_reward * 0.1)
        if explore < 0.15:
            return "ignore", 0.50, "Exploration"
        
        # Health + Reward Combined Logic
        combined_score = (health_score * 0.6) + (avg_reward * 0.4)
        if combined_score < 0.4:
            return "assign", confidence + 0.05, "System unstable - combined low"

        if avg_reward < 0.4:
            return "assign", confidence + 0.10, "Improving medium handling"

        return "assign", confidence, "Normal handling"

    else:  # low priority
        confidence = 0.90 + (avg_reward * 0.1)
        if explore < 0.20:
            return "assign", 0.50, "Exploration"
        
        # Health + Reward Combined Logic
        combined_score = (health_score * 0.7) + (avg_reward * 0.3)
        if combined_score < 0.3:
            return "assign", confidence - 0.10, "Low but system critical - combined"

        if avg_reward > 0.6:
            return "ignore", confidence - 0.20, "Low priority stable"

        return "ignore", confidence - 0.30, "Low priority"


# -------------------------------
# LOGGING (STRICT FORMAT)
# -------------------------------
def log_start(task, env, model):
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step, action, reward, done, error=None):
    error_val = error if error else "null"
    done_val = str(done).lower()

    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success, steps, rewards, avg_health, efficiency):
    rewards_str = ",".join([f"{r:.2f}" for r in rewards])

    print(
        f"[END] success={str(success).lower()} steps={steps} rewards={rewards_str}",
        flush=True,
    )


# -------------------------------
# MAIN EXECUTION
# -------------------------------
def run_baseline():
    env = OpsEnv()
    obs = env.reset()

    performance = {
        "high": [],
        "medium": [],
        "low": []
    }

    rewards = []
    steps = 0
    health_history = []

    # START LOG (MANDATORY)
    log_start("ai_ops_optimization", "ai_ops_env", "elite_agent_vFinal")

    try:
        while steps < 5:

            # SYSTEM HEALTH
            health_score = calculate_system_health(obs.tasks)
            health_history.append(health_score)

            # TASK PRIORITY ORDERING
            obs.tasks = sorted(
                obs.tasks,
                key=lambda t: {"high": 0, "medium": 1, "low": 2}[t.priority]
            )

            for task in obs.tasks:

                # SMART DECISION
                action_type, confidence, reason = smart_agent(task, health_score, performance)

                action = Action(
                    task_id=task.id,
                    action_type=action_type
                )

                obs, reward, done, _ = env.step(action)

                rewards.append(reward)
                performance[task.priority].append(reward)

                # EARLY EXIT
                if reward >= 1.0:
                    done = True

                # STRONG ACTION STRING (AI STYLE)
                action_str = (
                    f"{action_type}"
                    f"|p:{task.priority}"
                    f"|c:{confidence:.2f}"
                    f"|h:{health_score:.2f}"
                )

                # ✅ STEP LOG (STRICT)
                log_step(
                    step=steps + 1,
                    action=action_str,
                    reward=reward,
                    done=done,
                    error=None
                )

                if done:
                    break

            steps += 1

            if done:
                break

    except Exception as e:
        log_step(
            step=steps,
            action="error",
            reward=0.0,
            done=True,
            error=str(e)
        )

    finally:
        total_reward = sum(rewards)

        # ✅ SUCCESS
        success = total_reward > 0

        # 🔥 HEALTH METRIC
        avg_health = sum(health_history) / len(health_history) if health_history else 0

        # 🔥 EFFICIENCY METRIC
        efficiency = total_reward / (len(rewards) if rewards else 1)

        # ✅ END LOG (STRICT)
        log_end(success, steps, rewards, avg_health, efficiency)


# -------------------------------
# ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    run_baseline()
