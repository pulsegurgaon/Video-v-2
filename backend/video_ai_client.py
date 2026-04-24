import requests

# fallback (in case frontend not used)
DEFAULT_COLAB_API = "https://galore-wildland-faster.ngrok-free.dev/generate"


def generate_video(prompt, colab_url=None):
    """
    Sends prompt to AI video server (Colab)
    """

    url = colab_url if colab_url else DEFAULT_COLAB_API

    try:
        print(f"🎬 Sending to: {url}")

        res = requests.post(
            url,
            json={"prompt": prompt},
            timeout=300
        )

        data = res.json()

        print("✅ Video generated")
        return data

    except Exception as e:
        print("❌ Video API error:", e)
        return {
            "status": "error",
            "message": str(e)
        }