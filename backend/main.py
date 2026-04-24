from fastapi import FastAPI
import json, subprocess

app = FastAPI()

STATE = "state.json"

def load(): return json.load(open(STATE))
def save(d): json.dump(d, open(STATE,"w"), indent=4)

@app.post("/start")
def start():
    s = load()
    s["engine_running"] = True
    save(s)
    subprocess.Popen(["python3","automation.py"])
    return {"status":"started"}

@app.post("/stop")
def stop():
    s = load()
    s["engine_running"] = False
    save(s)
    return {"status":"stopped"}

@app.get("/queue")
def queue():
    return json.load(open("queue.json"))