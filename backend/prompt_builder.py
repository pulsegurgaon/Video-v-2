from ollama_client import ask_ollama
from groq_client import ask_groq
from storage_manager import load_state

def build_prompt(pillar, history):

    state = load_state()
    mode = state.get("llm_mode", "groq")

    if mode == "ollama":
        return ask_ollama(system, user)
    else:
        return ask_groq(system, user)

def build_prompt(pillar, history):

    idea_bank = {
        "dog": [
            "hungry puppy begging food at street stall",
            "lost puppy in rain at night",
            "dog saving human",
            "abandoned dog emotional"
        ],
        "satisfying": [
            "hydraulic press crushing objects",
            "shredder destroying items",
            "molten metal pouring",
            "perfect cleaning transformation"
        ],
        "survival": [
            "24 hours in snake room",
            "24 hours in ice room",
            "24 hours inside train",
            "24 hours in fire room"
        ],
        "restoration": [
            "rusty coin restoration",
            "old knife cleaning",
            "broken watch repair",
            "old car restoration"
        ],
        "whatif": [
            "lava meets ice",
            "glass melting",
            "metal freeze break",
            "magnet molten metal"
        ],
        "house": [
            "small house to luxury villa",
            "old house to modern",
            "empty land to house",
            "floor to interior design"
        ]
    }

    system = """
You are a viral short video director.

Generate a HIGH QUALITY AI video prompt.

Rules:
- 9:16 vertical
- cinematic
- 4K
- include camera movement
- include lighting
- include emotion or satisfaction
- no repetition
"""

    user = f"""
Category: {pillar}

Examples of user preference:
{idea_bank[pillar]}

Avoid repeating:
{history}

Create a NEW similar but unique idea and expand it into a cinematic video prompt.
"""

    return ask_ollama(system, user)