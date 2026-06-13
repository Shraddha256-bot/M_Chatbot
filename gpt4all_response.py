from gpt4all import GPT4All

model_name = "mistral-7b-openorca.Q4_0.gguf"
model = GPT4All(model_name)


def generate_gpt4all_response(
    user_input,
    emotion,
    history=None,
    persona="Friendly Bot 💖"
):
    persona_styles = {
        "Friendly Bot 💖": "You are warm, caring, and speak like a best friend.",
        "Calm Mentor 🧘": "You are wise, gentle, and give thoughtful advice.",
        "Cheerful Motivator ☀️": "You are upbeat, energetic, and encouraging.",
        "Romantic Companion 💌": "You are affectionate, supportive, and gentle."
    }

    style = persona_styles.get(persona, "")

    prompt = f"""
You are HarmoniChat.

Persona: {persona}
Style: {style}
Detected Emotion: {emotion}

Rules:
- Respond only as HarmoniChat.
- Do NOT generate user messages.
- Give only one response.
- Keep responses conversational and concise.
"""

    # Keep only recent history
    if history:
        history = history[-5:]

        for msg in history:
            role = msg["role"]

            if role == "user":
                prompt += f"\nUser: {msg['content']}"
            else:
                prompt += f"\nAssistant: {msg['content']}"

    prompt += f"\nUser: {user_input}\nAssistant:"

    print("Prompt length:", len(prompt))
    print("Generating response...")

    try:
        response = model.generate(
            prompt,
            max_tokens=80,
            temp=0.7,
            top_k=40,
            top_p=0.9
        )

        # Remove extra generated dialogue
        stop_tokens = [
            "User:",
            "Assistant:",
            "Human:",
            "\nUser",
            "\nAssistant"
        ]

        for token in stop_tokens:
            if token in response:
                response = response.split(token)[0]

        response = response.strip()

        print("Generation successful")

        if not response:
            response = "Hello! How can I help you today?"

        return response

    except Exception as e:
        print("GPT4All Error:", str(e))
        return "Sorry, I encountered an error while generating a response."


if __name__ == "__main__":
    reply = generate_gpt4all_response(
        "Hello",
        "joy",
        []
    )

    print("\nBOT RESPONSE:")
    print(reply)
