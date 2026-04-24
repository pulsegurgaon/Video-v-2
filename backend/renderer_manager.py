from video_ai_client import generate_video

def render_video(prompt, output):

    print("🎬 Generating real video...")

    video_file = generate_video(prompt)

    print(f"✅ Video ready: {video_file}")