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

/* BUTTONS */
.btn {
    display: inline-block;
    margin: 10px;
    padding: 14px 26px;
    background: linear-gradient(45deg, #00c6ff, #0072ff);
    color: white;
    text-decoration: none;
    border-radius: 12px;
    font-weight: bold;
    letter-spacing: 0.5px;
    position: relative;
    overflow: hidden;
    transition: all 0.4s ease;
}

/* Glow effect */
.btn:hover {
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 0 20px rgba(0,198,255,0.8),
                0 0 40px rgba(0,114,255,0.6);
}

/* Shine animation */
.btn::before {
    content: "";
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(
        120deg,
        transparent,
        rgba(255,255,255,0.4),
        transparent
    );
    transition: 0.6s;
}

.btn:hover::before {
    left: 100%;
}

/* CARDS */
.card {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(15px);
    margin: 15px;
    padding: 25px;
    border-radius: 18px;
    width: 260px;
    transition: all 0.4s ease;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Floating hover */
.card:hover {
    transform: translateY(-12px) scale(1.03);
    box-shadow: 0 15px 30px rgba(0,0,0,0.4);
}

/* HEADINGS */
h1 {
    font-size: 3.5em;
    margin-bottom: 10px;
    background: linear-gradient(90deg, #00c6ff, #ffffff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* TEXT */
p {
    font-size: 1.2em;
    opacity: 0.9;
}

/* CONTAINER */
.container {
    text-align: center;
    padding: 60px 20px;
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
    <p style="margin-top:10px;">
        🟢 System Live • Real-time AI Environment
    </p>
    <p>Next-generation AI system for intelligent task prioritization & autonomous decision making</p>
    <p style="margin-top:10px;">
        🟢 <b>System Status:</b> Running & Live
    </p>

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

    <div style="margin-top:60px;">

        <h2>⚙️ System Architecture</h2>
        <p>FastAPI-based backend simulating an AI-driven operational environment with task evaluation and scoring.</p>

        <div class="cards">
            <div class="card">
                <h3>📥 Input</h3>
                <p>Tasks with varying priorities enter the system.</p>
            </div>

            <div class="card">
                <h3>🧠 Decision Engine</h3>
                <p>AI selects actions like assign, escalate, or ignore.</p>
            </div>

            <div class="card">
                <h3>⚡ Environment</h3>
                <p>Simulates outcomes based on selected actions.</p>
            </div>

            <div class="card">
                <h3>📊 Grader</h3>
                <p>Returns reward score between 0 and 1.</p>
            </div>
        </div>

    </div>

    <div style="margin-top:60px;">
        <h2>🚀 How It Works</h2>

        <div class="cards">
            <div class="card">
                <h3>1️⃣ Reset</h3>
                <p>Initialize environment state.</p>
            </div>

            <div class="card">
                <h3>2️⃣ Step</h3>
                <p>Agent performs action on task.</p>
            </div>

            <div class="card">
                <h3>3️⃣ Evaluate</h3>
                <p>System calculates reward score.</p>
            </div>

            <div class="card">
                <h3>4️⃣ Optimize</h3>
                <p>Improve decisions using feedback loop.</p>
            </div>
        </div>
    </div>

    <div style="margin-top:60px;">
        <h2>📊 Live System Metrics</h2>

        <div class="cards">
            <div class="card">
                <h3>⚡ Active Tasks</h3>
                <p id="taskCount">Loading...</p>
            </div>

            <div class="card">
                <h3>🎯 Avg Score</h3>
                <p id="score">Loading...</p>
            </div>

            <div class="card">
                <h3>🔄 Steps Executed</h3>
                <p id="steps">Real-time</p>
            </div>
        </div>
    </div>

    <div style="margin-top:60px;">
        <h2>💡 Why This is Innovative</h2>

        <div class="cards">
            <div class="card">
                <h3>🧠 Agent Training Environment</h3>
                <p>Not just an app — a system to train intelligent decision-making agents.</p>
            </div>

            <div class="card">
                <h3>⚙️ OpenEnv Based</h3>
                <p>Follows standardized environment design for AI evaluation.</p>
            </div>

            <div class="card">
                <h3>📊 Reward-driven Learning</h3>
                <p>Actions are evaluated using normalized scoring for optimization.</p>
            </div>

            <div class="card">
                <h3>🚀 Real-world Simulation</h3>
                <p>Replicates operational workflows like DevOps & support systems.</p>
            </div>
        </div>
    </div>

    <div style="margin-top:60px;">
        <h2>🌍 Real-world Applications</h2>

        <div class="cards">
            <div class="card">
                <h3>🛠 DevOps</h3>
                <p>Automated incident prioritization and resolution.</p>
            </div>

            <div class="card">
                <h3>💬 Customer Support</h3>
                <p>AI-driven ticket handling and escalation.</p>
            </div>

            <div class="card">
                <h3>🏢 Enterprise Ops</h3>
                <p>Workflow automation and decision optimization.</p>
            </div>
        </div>
    </div>

    <footer style="margin-top:60px; opacity:0.7;">
        Built by Ganesh • OpenEnv Hackathon 🚀 <br>
        🌐 <a href="/docs" target="_blank" style="color:#00c6ff;">API Docs</a>
    </footer>

</div>

<script>
async function loadMetrics() {
    try {
        const res = await fetch('/baseline');
        const data = await res.json();

        document.getElementById('score').innerText = data.average_score || "0.0";
        document.getElementById('steps').innerText = data.steps || "N/A";
    } catch (e) {
        document.getElementById('score').innerText = "Error";
    }

    try {
        const taskRes = await fetch('/tasks');
        const tasks = await taskRes.json();
        document.getElementById('taskCount').innerText = tasks.length;
    } catch (e) {
        document.getElementById('taskCount').innerText = "Error";
    }
}

loadMetrics();
</script>

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