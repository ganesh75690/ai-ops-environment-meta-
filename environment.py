from models import Action, Observation
from grader import grade_easy, grade_medium
from state import EnvState

class OpsEnv:
    def __init__(self):
        self.state = EnvState()
        self.reset()

    def reset(self):
        self.state.reset()
        return Observation(tasks=self.state.tasks, message="Environment reset")

    def step(self, action: Action):
        self.state.step_count += 1

        task = next((t for t in self.state.tasks if t.id == action.task_id), None)

        if not task:
            return Observation(tasks=self.state.tasks, message="Invalid task"), -1, True, {}

        # Use grader instead of simple logic
        reward = grade_easy(action, task)

        # small penalty for bad action
        if action.action_type == "ignore" and task.priority == "high":
            reward -= 0.5

        reward = max(0.0, min(reward, 1.0))

        done = self.state.step_count >= 5

        return Observation(tasks=self.state.tasks, message="Step executed"), reward, done, {}

    def state_view(self):
        return self.state.tasks