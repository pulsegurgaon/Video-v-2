import time, json
from prompt_builder import build_prompt
from renderer_manager import render_video
from drive_uploader import upload_to_drive
from notifier import remind_upload

STATE = "state.json"
QUEUE = "queue.json"

def load(f): return json.load(open(f))
def save(f,d): json.dump(d, open(f,"w"), indent=4)

def run():

    while True:
        s = load(STATE)

        if not s["engine_running"]:
            time.sleep(2)
            continue

        idx = s["total_videos"] % len(s["pillars"])
        pillar = s["pillars"][idx]

        print(f"\n🧠 Generating: {pillar}")

        prompt = build_prompt(pillar, s["history"])

        file = f"video_{s['total_videos']+1}.mp4"

        render_video(prompt, file)

        name = upload_to_drive(file)
        remind_upload(name)

        q = load(QUEUE)
        q.append({"pillar": pillar, "prompt": prompt[:80]})
        save(QUEUE, q)

        s["history"].append(prompt[:50])
        s["total_videos"] += 1
        save(STATE, s)

        time.sleep(2)