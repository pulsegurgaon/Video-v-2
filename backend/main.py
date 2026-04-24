from fastapi import FastAPI
import json, subprocess, os
from datetime import datetime
from prompt_builder import build_prompt

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
# INIT STATE
# ---------------------------
if not os.path.exists(STATE):
    save(STATE, {
        "engine_running": False,
        "gpu_mode": "ovh",
        "history": [],
        "pillar_index": 0,
        "pillars": [
            "dog",
            "satisfying",
            "survival",
            "restoration",
            "whatif",
            "house"
        ]
    })

if not os.path.exists(QUEUE):
    save(QUEUE, [])

# ---------------------------
# ROTATION
# ---------------------------
def get_next_pillar():
    state = load(STATE)

    pillars = state["pillars"]
    index = state["pillar_index"]

    pillar = pillars[index]

    # rotate
    state["pillar_index"] = (index + 1) % len(pillars)
    save(STATE, state)

    return pillar

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

    subprocess.Popen(["python3", os.path.join(BASE, "automation.py")])

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
# 🔥 AUTO GENERATION (NO INPUT NEEDED)
# ---------------------------
@app.post("/generate")
def generate():

    state = load(STATE)
    history = state["history"]

    pillar = get_next_pillar()

    # 🧠 YOUR OLLAMA SYSTEM
    prompt = build_prompt(pillar, history)

    job = {
        "pillar": pillar,
        "prompt": prompt,
        "status": "pending",
        "time": str(datetime.now())
    }

    q = load(QUEUE)
    q.append(job)
    save(QUEUE, q)

    # update history
    history.append(prompt[:80])
    state["history"] = history[-20:]
    save(STATE, state)

    return {
        "status": "generated 🔥",
        "pillar": pillar,
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

# ---------------------------
# EDIT PILLARS (FROM FRONTEND)
# ---------------------------
@app.post("/pillars")
def update_pillars(data: dict):
    new_pillars = data.get("pillars")

    if not new_pillars or len(new_pillars) == 0:
        return {"error": "invalid pillars"}

    state = load(STATE)
    state["pillars"] = new_pillars
    state["pillar_index"] = 0  # reset rotation

    save(STATE, state)

    return {"status": "updated"}
@app.post("/set-delay/{seconds}")
def set_delay(seconds: int):
    s = load()
    s["delay"] = seconds
    save(s)
    return {"delay": seconds}