import time
from prompt_builder import build_prompt
from renderer_manager import render_video
from drive_uploader import upload_to_drive
from notifier import remind_upload

from storage_manager import (
    load_state,
    save_state,
    load_queue,
    save_queue
)

def run_engine():

    print("🚀 Automation Engine Started...")

    while True:
        state = load_state()

        # ⛔ Engine OFF
        if not state["engine_running"]:
            time.sleep(2)
            continue

        pillars = state["pillars"]

        # 🔁 ROTATION
        index = state["total_videos"] % len(pillars)
        pillar = pillars[index]

        print(f"\n🧠 Current Pillar: {pillar}")

        try:
            # 🧠 AI Prompt
            prompt = build_prompt(pillar, state["history"])

        except Exception as e:
            print("❌ Ollama error:", e)
            time.sleep(3)
            continue

        file_name = f"video_{state['total_videos'] + 1}.mp4"

        try:
            # 🎥 Render
            render_video(prompt, file_name)

        except Exception as e:
            print("❌ Render error:", e)
            time.sleep(3)
            continue

        # ☁️ Upload
        uploaded_name = upload_to_drive(file_name)

        # 🔔 Notify
        remind_upload(uploaded_name)

        # 📦 Queue update
        queue = load_queue()
        queue.append({
            "id": state["total_videos"] + 1,
            "pillar": pillar,
            "file": uploaded_name,
            "prompt": prompt[:120]
        })
        save_queue(queue)

        # 🧠 Memory
        state["history"].append(prompt[:80])

        # 🔢 Count
        state["total_videos"] += 1

        # 💾 Save
        save_state(state)

        print(f"✅ Video {state['total_videos']} completed")

        # ⚡ DYNAMIC SPEED CONTROL
        delay = state.get("delay", 2)
        print(f"⏳ Waiting {delay}s before next video...\n")
        time.sleep(delay)