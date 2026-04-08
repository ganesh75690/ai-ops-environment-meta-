from typing import List
import random
from ai_ops_env.models import Task

# Explicit task definitions
TASKS = [
    {
        "id": 1,
        "name": "load_balancing_optimization",
        "difficulty": "medium",
        "description": "Optimize load distribution across servers"
    },
    {
        "id": 2,
        "name": "anomaly_detection_monitoring",
        "difficulty": "medium",
        "description": "Detect unusual patterns in system metrics"
    },
    {
        "id": 3,
        "name": "resource_allocation_planning",
        "difficulty": "medium",
        "description": "Plan optimal resource allocation strategies"
    },
    {
        "id": 4,
        "name": "incident_response_automation",
        "difficulty": "hard",
        "description": "Automate incident detection and response workflows"
    },
    {
        "id": 5,
        "name": "performance_tuning_engine",
        "difficulty": "hard",
        "description": "Tune system performance parameters"
    },
    {
        "id": 6,
        "name": "cost_efficiency_optimization",
        "difficulty": "hard",
        "description": "Optimize costs while maintaining performance"
    },
    {
        "id": 7,
        "name": "intelligent_scheduling_system",
        "difficulty": "medium",
        "description": "Intelligent task scheduling and prioritization"
    },
    {
        "id": 8,
        "name": "database_performance_tuning",
        "difficulty": "hard",
        "description": "Optimize database queries and indexing for better performance"
    },
    {
        "id": 9,
        "name": "basic_system_monitoring",
        "difficulty": "easy",
        "description": "Monitor basic system health and status"
    },
    {
        "id": 10,
        "name": "simple_log_analysis",
        "difficulty": "easy",
        "description": "Analyze basic system logs for errors"
    }
]

class EnvState:
    def __init__(self):
        self.tasks: List[Task] = []
        self.step_count = 0
        self.current_task = None

    def reset(self):
        # Select random task from explicit task list
        self.current_task = random.choice(TASKS)
        
        base_tasks = [
            Task(id=1, description="load_balancing_optimization", priority="medium"),
            Task(id=2, description="anomaly_detection_monitoring", priority="medium"),
            Task(id=3, description="resource_allocation_planning", priority="medium"),
            Task(id=4, description="incident_response_automation", priority="high"),
            Task(id=5, description="performance_tuning_engine", priority="high"),
            Task(id=6, description="cost_efficiency_optimization", priority="high"),
            Task(id=7, description="intelligent_scheduling_system", priority="medium"),
            Task(id=8, description="database_performance_tuning", priority="high"),
            Task(id=9, description="basic_system_monitoring", priority="low"),
            Task(id=10, description="simple_log_analysis", priority="low"),
        ]

        # random shuffle (adds realism)
        random.shuffle(base_tasks)

        self.tasks = base_tasks
        self.step_count = 0
