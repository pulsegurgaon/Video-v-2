import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # set this in environment

URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_groq(system, user):

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",  # fast + strong
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ],
        "temperature": 0.9
    }

    try:
        res = requests.post(URL, headers=headers, json=data, timeout=30)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]

    except Exception as e:
        print("❌ Groq error:", e)
        return "cinematic video, 4K, dramatic lighting, fallback prompt"