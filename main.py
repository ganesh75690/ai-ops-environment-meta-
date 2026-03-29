from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from environment import OpsEnv
from models import Action
from tasks import get_tasks
from grader import grade_easy
from baseline import run_baseline

app = FastAPI()
env = OpsEnv()

@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Ops Intelligence</title>

<style>
    body {
        margin: 0;
        font-family: 'Segoe UI', sans-serif;
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
    }

    .container {
        text-align: center;
        padding: 60px 20px;
    }

    h1 {
        font-size: 3.5em;
        margin-bottom: 10px;
        animation: fadeInDown 1s ease-in-out;
    }

    p {
        font-size: 1.2em;
        opacity: 0.9;
        animation: fadeIn 2s ease-in-out;
    }

    .buttons {
        margin-top: 30px;
    }

    .btn {
        display: inline-block;
        margin: 10px;
        padding: 14px 24px;
        background: #00c6ff;
        background: linear-gradient(45deg, #00c6ff, #0072ff);
        color: white;
        text-decoration: none;
        border-radius: 10px;
        font-weight: bold;
        transition: 0.3s;
    }

    .btn:hover {
        transform: scale(1.1);
        box-shadow: 0 0 15px #00c6ff;
    }

    .cards {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        margin-top: 50px;
    }

    .card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        margin: 15px;
        padding: 25px;
        border-radius: 15px;
        width: 260px;
        transition: 0.3s;
    }

    .card:hover {
        transform: translateY(-10px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
    }

    footer {
        margin-top: 60px;
        opacity: 0.7;
        font-size: 0.9em;
    }

    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }

    @keyframes fadeInDown {
        from {opacity: 0; transform: translateY(-20px);}
        to {opacity: 1; transform: translateY(0);}
    }
</style>
</head>

<body>

<div class="container">

    <h1>🚀 AI Ops Intelligence</h1>
    <p>Autonomous AI system for task prioritization & decision making</p>

    <div class="buttons">
        <a class="btn" href="/docs">📘 API Docs</a>
        <a class="btn" href="/tasks">📋 Tasks</a>
        <a class="btn" href="/baseline">⚡ Baseline</a>
        <a class="btn" href="/state">📊 State</a>
    </div>

    <div class="cards">
        <div class="card">
            <h3>🧠 Smart Decisions</h3>
            <p>AI selects optimal actions based on priority and rewards.</p>
        </div>

        <div class="card">
            <h3>⚡ Real-time Simulation</h3>
            <p>Environment reacts dynamically to each step execution.</p>
        </div>

        <div class="card">
            <h3>📊 Performance Scoring</h3>
            <p>Grader evaluates actions and returns normalized scores.</p>
        </div>

        <div class="card">
            <h3>🔁 Reinforcement Ready</h3>
            <p>Built for scalable RL-based optimization workflows.</p>
        </div>
    </div>

    <footer>
        Built by Ganesh • OpenEnv Hackathon 🚀
    </footer>

</div>

</body>
</html>
"""

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