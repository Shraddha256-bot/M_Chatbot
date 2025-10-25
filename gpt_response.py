import openai
import os
from dotenv import load_dotenv

load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_gpt_response(user_input, emotion):
    prompt = f"""
You are an emotionally intelligent AI chatbot that replies empathetically based on the user's emotion.
The user is feeling {emotion}. Respond supportively and naturally like a friend or counselor.

User: {user_input}
AI:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You're a supportive, friendly emotional chatbot."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()
