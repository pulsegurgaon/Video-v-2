from fastapi import FastAPI
import json, subprocess, os
from datetime import datetime

app = FastAPI()

BASE = os.path.dirname(__file__)
STATE = os.path.join(BASE, "state.json")
QUEUE = os.path.join(BASE, "queue.json")

# ---------------------------
# SAFE LOAD / SAVE
# ---------------------------
def load(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        return json.load(f)

def save(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# ---------------------------
# DEFAULT FILES INIT
# ---------------------------
if not os.path.exists(STATE):
    save(STATE, {
        "engine_running": False,
        "last_run": None
    })

if not os.path.exists(QUEUE):
    save(QUEUE, [])

# ---------------------------
# ROUTES
# ---------------------------

@app.get("/")
def home():
    return {"message": "AI Engine is Running 🚀"}

@app.get("/status")
def status():
    s = load(STATE, {})
    return {
        "running": s.get("engine_running", False),
        "last_run": s.get("last_run")
    }

@app.post("/start")
def start():
    s = load(STATE, {})
    s["engine_running"] = True
    s["last_run"] = str(datetime.now())
    save(STATE, s)

    subprocess.Popen(["python3", os.path.join(BASE, "automation.py")])

    return {"status": "started 🚀"}

@app.post("/stop")
def stop():
    s = load(STATE, {})
    s["engine_running"] = False
    save(STATE, s)

    return {"status": "stopped 🛑"}

@app.get("/queue")
def queue():
    return load(QUEUE, [])

@app.post("/add")
def add_to_queue(item: dict):
    q = load(QUEUE, [])
    item["time"] = str(datetime.now())
    q.append(item)
    save(QUEUE, q)
    return {"status": "added", "queue_size": len(q)}