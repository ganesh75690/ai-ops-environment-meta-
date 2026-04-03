from typing import List
import random
from ai_ops_env.models import Task

class EnvState:
    def __init__(self):
        self.tasks: List[Task] = []
        self.step_count = 0

    def reset(self):
        base_tasks = [
            Task(id=1, description="Server down", priority="high"),
            Task(id=2, description="Feature request", priority="low"),
            Task(id=3, description="Payment issue", priority="medium"),
        ]

        # random shuffle (adds realism)
        random.shuffle(base_tasks)

        self.tasks = base_tasks
        self.step_count = 0
