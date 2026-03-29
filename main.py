from fastapi import FastAPI
from environment import OpsEnv
from models import Action
from tasks import get_tasks
from grader import grade_easy
from baseline import run_baseline

app = FastAPI()
env = OpsEnv()

@app.get("/")
def home():
    return {"message": "AI Ops Environment is running 🚀"}

@app.get("/reset")
def reset():
    return env.reset()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state_view()

@app.get("/tasks")
def tasks():
    return get_tasks()

@app.post("/grader")
def grader_endpoint(action: Action):
    task = next((t for t in env.state.tasks if t.id == action.task_id), None)

    if not task:
        return {"score": 0.0}

    score = grade_easy(action, task)
    return {"score": score}

@app.get("/baseline")
def baseline():
    return run_baseline()