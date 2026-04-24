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

        # ⛔ STOP if not running
        if not state["engine_running"]:
            time.sleep(2)
            continue

        pillars = state["pillars"]

        # 🔁 ROTATION LOGIC
        index = state["total_videos"] % len(pillars)
        pillar = pillars[index]

        print(f"\n🧠 Current Pillar: {pillar}")

        try:
            # 🧠 BUILD PROMPT FROM OLLAMA
            prompt = build_prompt(pillar, state["history"])

        except Exception as e:
            print("❌ Ollama error:", e)
            time.sleep(3)
            continue

        # 🎬 OUTPUT FILE
        file_name = f"video_{state['total_videos'] + 1}.mp4"

        try:
            # 🎥 RENDER VIDEO
            render_video(prompt, file_name)

        except Exception as e:
            print("❌ Render error:", e)
            time.sleep(3)
            continue

        # ☁️ SAVE TO STORAGE
        uploaded_name = upload_to_drive(file_name)

        # 🔔 REMIND USER
        remind_upload(uploaded_name)

        # 📦 UPDATE QUEUE
        queue = load_queue()
        queue.append({
            "id": state["total_videos"] + 1,
            "pillar": pillar,
            "file": uploaded_name,
            "prompt": prompt[:120]
        })
        save_queue(queue)

        # 🧠 SAVE HISTORY (ANTI-REPEAT)
        state["history"].append(prompt[:80])

        # 🔢 INCREMENT COUNT
        state["total_videos"] += 1

        # 💾 SAVE STATE (CRASH PROOF)
        save_state(state)

        print(f"✅ Video {state['total_videos']} completed\n")

        # ⏳ WAIT
        time.sleep(2)