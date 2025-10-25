from gpt4all import GPT4All

model_name = "mistral-7b-openorca.Q4_0.gguf"  # replace with your exact model file name
model = GPT4All(model_name)

def generate_gpt4all_response(user_input, emotion, history=None, persona="Friendly Bot 💖"):
    # Define styles for each persona
    persona_styles = {
        "Friendly Bot 💖": "You're warm, caring, and speak like a best friend.",
        "Calm Mentor 🧘": "You're wise, gentle, and give thoughtful, calm advice.",
        "Cheerful Motivator ☀️": "You're upbeat, energetic, and encourage the user with a positive spirit.",
        "Romantic Companion 💌": "You respond with soft, affectionate tones — like a supportive partner."
    }

    style = persona_styles.get(persona, "")
    prompt = f"You are HarmoniChat, a chatbot who responds as: {persona}.\n{style}\nThe user is feeling {emotion}."


    # Add conversation history
    if history:
        for msg in history:
            prompt += f"\n{msg['role'].capitalize()}: {msg['content']}"

    prompt += f"\nUser: {user_input}\nAI:"

    with model.chat_session():
        response = model.generate(prompt, max_tokens=150)

    return response.strip()
