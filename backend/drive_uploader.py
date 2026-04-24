import time

def upload_to_drive(file):
    name = f"video_{int(time.time())}.mp4"
    print(f"☁️ Saved: {name}")
    return name