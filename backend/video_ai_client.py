import time
import os

OUTPUT_DIR = "outputs"

# make sure folder exists
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)


def generate_video(prompt, output_file):
    """
    This function will:
    1. Receive prompt from backend
    2. Send to video AI (later)
    3. Return final video file path
    """

    print("\n🎬 [VIDEO AI] Generating video...")
    print("🧠 Prompt received:\n")
    print(prompt)

    # ⚠️ CURRENT MODE: FAKE RENDER (SAFE TEST MODE)
    # This avoids wasting GPU time while testing

    fake_path = os.path.join(OUTPUT_DIR, output_file)

    with open(fake_path, "w") as f:
        f.write("FAKE VIDEO FILE\n")
        f.write(prompt)

    time.sleep(2)

    print(f"\n✅ [VIDEO AI] Video created: {fake_path}")

    return fake_path


# 🚀 FUTURE (REAL VIDEO AI HOOK)
def generate_video_real(prompt):
    """
    Later we replace this with:
    - ComfyUI API
    - AnimateDiff
    - SkyReels
    """

    # Example structure (not active yet)
    """
    import requests

    response = requests.post("http://localhost:8188/prompt", json={
        "prompt": prompt
    })

    return response.json()["video"]
    """

    pass