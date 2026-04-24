from fastapi import FastAPI
import json, subprocess, os
from datetime import datetime

from prompt_builder import build_prompt   # 👈 YOUR FILE

app = FastAPI()

BASE = os.path.dirname(__file__)
STATE = os.path.join(BASE, "backend/state.json")
QUEUE = os.path.join(BASE, "backend/queue.json")

# ---------------------------
# FILE HANDLING
# ---------------------------
def load(file):
    if not os.path.exists(file):
        return {} if file == STATE else []
    with open(file, "r") as f:
        return json.load(f)

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# ---------------------------
# INIT
# ---------------------------
if not os.path.exists(STATE):
    save(STATE, {
        "engine_running": False,
        "gpu_mode": "ovh",
        "history": []
    })

if not os.path.exists(QUEUE):
    save(QUEUE, [])

# ---------------------------
# ROUTES
# ---------------------------

@app.get("/")
def home():
    return {"message": "AI Engine Running 🚀"}

@app.get("/status")
def status():
    return load(STATE)

@app.post("/start")
def start():
    s = load(STATE)
    s["engine_running"] = True
    save(STATE, s)

    subprocess.Popen(["python3", os.path.join(BASE, "backend/automation.py")])

    return {"status": "started"}

@app.post("/stop")
def stop():
    s = load(STATE)
    s["engine_running"] = False
    save(STATE, s)

    return {"status": "stopped"}

@app.get("/queue")
def queue():
    return load(QUEUE)

# ---------------------------
# 🔥 CORE: ADD JOB USING OLLAMA
# ---------------------------
@app.post("/add")
def add_to_queue(data: dict):

    pillar = data.get("type")

    if not pillar:
        return {"error": "pillar required"}

    state = load(STATE)
    history = state.get("history", [])

    # 🧠 Generate prompt using YOUR prompt_builder
    prompt = build_prompt(pillar, history)

    job = {
        "pillar": pillar,
        "prompt": prompt,
        "status": "pending",
        "time": str(datetime.now())
    }

    # save queue
    q = load(QUEUE)
    q.append(job)
    save(QUEUE, q)

    # update history (store short version to avoid repetition)
    history.append(prompt[:80])
    state["history"] = history[-20:]  # keep last 20 only
    save(STATE, state)

    return {
        "status": "generated via ollama 🧠🔥",
        "prompt": prompt
    }

# ---------------------------
# MODE SWITCH
# ---------------------------
@app.post("/mode/{mode}")
def set_mode(mode: str):

    if mode not in ["ovh", "colab"]:
        return {"error": "invalid mode"}

    s = load(STATE)
    s["gpu_mode"] = mode
    save(STATE, s)

    return {"mode": mode}