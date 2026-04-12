from pydantic import BaseModel
from typing import List

class Task(BaseModel):
    id: str
    description: str
    priority: str

class Action(BaseModel):
    task_id: str
    action_type: str  # assign / escalate / ignore

class Observation(BaseModel):
    tasks: List[Task]
    message: str
