from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

import os, json, threading, time
from datetime import datetime

from prompt_builder import build_prompt
from video_ai_client import generate_video

app = FastAPI()

# -----------------------
# PATH SETUP
# -----------------------
BASE = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(BASE, "..", "frontend")

STATE_FILE = os.path.join(BASE, "state.json")
QUEUE_FILE = os.path.join(BASE, "queue.json")

# -----------------------
# SERVE FRONTEND 🎮
# -----------------------
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_ui():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "AI Engine Running 🚀 (no frontend found)"}

# -----------------------
# FILE HANDLING
# -----------------------
def load(file, default):
    if not os.path.exists(file):
        return default
    with open(file, "r") as f:
        return json.load(f)

def save(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)

# -----------------------
# INIT DEFAULT STATE
# -----------------------
if not os.path.exists(STATE_FILE):
    save(STATE_FILE, {
        "engine_running": False,
        "llm_mode": "groq",
        "colab_url": "",
        "pillars": ["dog", "satisfying", "survival", "restoration", "whatif", "house"],
        "history": [],
        "total_videos": 0,
        "last_run": None
    })

if not os.path.exists(QUEUE_FILE):
    save(QUEUE_FILE, [])

# -----------------------
# REQUEST MODEL
# -----------------------
class Config(BaseModel):
    colab_url: str | None = None
    llm_mode: str | None = None
    pillars: list[str] | None = None

# -----------------------
# CORE ENGINE LOOP 🔥
# -----------------------
def engine_loop():

    print("🚀 Engine Started...")

    while True:
        state = load(STATE_FILE, {})

        if not state.get("engine_running"):
            time.sleep(2)
            continue

        pillars = state["pillars"]

        # rotation logic
        index = state["total_videos"] % len(pillars)
        pillar = pillars[index]

        print(f"\n🧠 Pillar: {pillar}")

        # ---------------- PROMPT ----------------
        try:
            prompt = build_prompt(pillar, state["history"])
            print("🎯 Prompt:", prompt[:100])

        except Exception as e:
            print("❌ Prompt error:", e)
            time.sleep(3)
            continue

        # ---------------- VIDEO ----------------
        try:
            res = generate_video(prompt, state.get("colab_url"))

        except Exception as e:
            print("❌ Video error:", e)
            time.sleep(3)
            continue

        # ---------------- QUEUE ----------------
        queue = load(QUEUE_FILE, [])
        queue.append({
            "id": state["total_videos"] + 1,
            "pillar": pillar,
            "prompt": prompt[:120],
            "time": str(datetime.now())
        })
        save(QUEUE_FILE, queue)

        # ---------------- STATE UPDATE ----------------
        state["history"].append(prompt[:80])
        state["total_videos"] += 1
        state["last_run"] = str(datetime.now())

        save(STATE_FILE, state)

        print(f"✅ Video {state['total_videos']} done")

        time.sleep(5)

# -----------------------
# START ENGINE THREAD
# -----------------------
threading.Thread(target=engine_loop, daemon=True).start()

# -----------------------
# ROUTES 🎮
# -----------------------

@app.get("/status")
def status():
    return load(STATE_FILE, {})

@app.post("/start")
def start():
    state = load(STATE_FILE, {})
    state["engine_running"] = True
    save(STATE_FILE, state)
    return {"status": "started 🚀"}

@app.post("/stop")
def stop():
    state = load(STATE_FILE, {})
    state["engine_running"] = False
    save(STATE_FILE, state)
    return {"status": "stopped 🛑"}

@app.get("/queue")
def queue():
    return load(QUEUE_FILE, [])

@app.post("/config")
def update_config(cfg: Config):
    state = load(STATE_FILE, {})

    if cfg.colab_url is not None:
        state["colab_url"] = cfg.colab_url

    if cfg.llm_mode is not None:
        state["llm_mode"] = cfg.llm_mode

    if cfg.pillars is not None:
        state["pillars"] = cfg.pillars

    save(STATE_FILE, state)

    return {"status": "updated ⚙️"}