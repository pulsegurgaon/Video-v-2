import requests
import time

# 🔗 UPDATE THIS EVERY TIME COLAB RESTARTS
BASE_URL = "https://galore-wildland-faster.ngrok-free.dev"
GENERATE_API = BASE_URL + "/generate"


def generate_video(prompt, output_file):
    try:
        print("☁️ Sending prompt to AI Video Server...")
        
        res = requests.post(
            GENERATE_API,
            json={"prompt": prompt},
            timeout=600
        )

        data = res.json()

        if data.get("status") != "done":
            raise Exception("Generation failed")

        video_url = BASE_URL + data["video_url"]

        print("⬇️ Downloading video...")
        
        video_data = requests.get(video_url).content

        with open(output_file, "wb") as f:
            f.write(video_data)

        print(f"✅ Saved: {output_file}")
        return output_file

    except Exception as e:
        print("❌ Error:", e)
        return None