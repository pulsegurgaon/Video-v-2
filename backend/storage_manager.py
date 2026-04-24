import json
import os
import threading

STATE_FILE = "state.json"
QUEUE_FILE = "queue.json"

lock = threading.Lock()

def safe_read(file, default):
    if not os.path.exists(file):
        return default
    with open(file, "r") as f:
        return json.load(f)

def safe_write(file, data):
    with lock:
        with open(file, "w") as f:
            json.dump(data, f, indent=4)

def load_state():
    return safe_read(STATE_FILE, {
        "engine_running": False,
        "total_videos": 0,
        "gpu_mode": "auto",
        "pillars": ["dog","satisfying","survival","restoration","whatif","house"],
        "history": []
    })

def save_state(state):
    safe_write(STATE_FILE, state)

def load_queue():
    return safe_read(QUEUE_FILE, [])

def save_queue(queue):
    safe_write(QUEUE_FILE, queue)