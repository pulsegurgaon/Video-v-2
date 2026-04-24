import json

STATE = "state.json"

def get_mode():
    return json.load(open(STATE))["gpu_mode"]

def generate_video(prompt):
    mode = get_mode()

    if mode == "ovh":
        return generate_local(prompt)

    elif mode == "colab":
        return trigger_colab(prompt)


def generate_local(prompt):
    print("🔥 Running on OVH GPU")
    # TODO: connect your actual video AI here
    return "video_generated_locally.mp4"


def trigger_colab(prompt):
    print("☁️ Sending job to Colab")

    # TODO:
    # - send prompt to Colab notebook (API / webhook / shared file)
    # - wait or return link

    return "colab_video_link.mp4"