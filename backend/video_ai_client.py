import requests
from storage_manager import load_state

# 🔗 PUT YOUR COLAB NGROK LINK HERE
COLAB_API = "https://your-ngrok-url.ngrok-free.app/generate"


def generate_video(prompt, output_file):

    state = load_state()
    mode = state.get("gpu_mode", "colab")

    print(f"⚙️ Mode: {mode}")

    # ☁️ COLAB MODE (PRIMARY WORKING SYSTEM)
    if mode == "colab":

        print("☁️ Sending prompt to Colab...")

        try:
            res = requests.post(COLAB_API, json={
                "prompt": prompt
            }, timeout=300)

            if res.status_code != 200:
                raise Exception(f"Bad response: {res.text}")

            data = res.json()
            video_url = data.get("video_url")

            if not video_url:
                raise Exception("No video_url returned")

            print("⬇️ Downloading video...")

            video_data = requests.get(video_url).content

            with open(output_file, "wb") as f:
                f.write(video_data)

            print(f"✅ Video saved: {output_file}")

            return output_file

        except Exception as e:
            print("❌ Colab error:", e)
            return None

    # ⚡ OVH MODE (placeholder until you install real model)
    elif mode == "ovh":
        print("⚠️ OVH mode selected but no model connected yet")
        raise Exception("No local video model installed")

    else:
        raise Exception("Invalid mode")