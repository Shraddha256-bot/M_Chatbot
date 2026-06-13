import streamlit as st
from transformers import pipeline
import speech_recognition as sr
import pyttsx3
from gpt4all_response import generate_gpt4all_response
from db import init_db, log_mood, get_mood_history
from deep_translator import GoogleTranslator
import matplotlib.pyplot as plt

# =============== INIT =================
init_db()

# ============== Sidebar ==============
with st.sidebar:
    st.header("👤 Your Profile")
    username = st.text_input("Name", value="Shraddha")
    age = st.number_input("Age", min_value=10, max_value=100, value=21)
    music_pref = st.selectbox("Preferred Music Genre", ["Lo-fi", "Classical", "Jazz", "Bollywood", "Instrumental"])
    language_choice = st.selectbox("🌍 Preferred Language", ["English", "Hindi"])

# =========== Mood Warning Logic ===========
def detect_low_mood_streak(history):
    emotions = [e for _, e in history[-3:]]
    if emotions.count("sadness") >= 2 or emotions.count("fear") >= 2:
        return "⚠️ You’ve been feeling low lately. Maybe take a break or talk to someone?"
    return None

# =========== Load Emotion Classifier ===========
@st.cache_resource
def load_model():
    return pipeline("text-classification",
                    model="bhadresh-savani/distilbert-base-uncased-emotion",
                    return_all_scores=True, device=-1)

emotion_classifier = load_model()

# =========== Voice Input ===========
def listen_to_voice():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎧 Speak now...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            st.success(f"🗣 You said: {text}")
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I couldn't understand your voice.")
        except sr.RequestError:
            st.error("Voice recognition failed. Check your internet.")

# =========== Speak Output ===========
def speak_response(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    engine.say(text)
    engine.runAndWait()

# =========== Emotion Detection ===========
def detect_emotion(text):
    results = emotion_classifier(text)[0]
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[0]['label'], results[0]['score']

# =========== Music Suggestion ===========
def suggest_music(emotion_label):
    emotion_music_map = {
        'joy': "https://www.youtube.com/watch?v=Uy5VCOnqdAo",
        'sadness': "https://www.youtube.com/watch?v=07DLCDhDfM8",
        'anger': "https://www.youtube.com/watch?v=2_BVk4AI4zI",
        'surprise': "https://www.youtube.com/watch?v=0oCwcZy4pVM",
        'disgust': "https://www.youtube.com/watch?v=QJO3ROT-A4E",
        'fear': "https://www.youtube.com/shorts/z2m8b8aMQtw",
        'neutral': "https://www.youtube.com/watch?v=EfcJevM_aWY",
        'love': "https://www.youtube.com/watch?v=tB8N3hzfCZo"
    }
    return emotion_music_map.get(emotion_label.lower(), "https://www.youtube.com/watch?v=DWcJFNfaw9c")

# =========== Short Reply Detection ===========
def get_short_reply(text):
    thank_keywords = ["thank you", "thanks", "thx", "grateful", "appreciate"]
    okay_keywords = ["okay", "ok", "sure", "fine"]
    bye_keywords = ["bye", "goodbye", "see you"]

    lowered = text.lower()
    if any(kw in lowered for kw in thank_keywords):
        return "You're welcome! 😊"
    elif any(kw in lowered for kw in okay_keywords):
        return "Alright! Let me know if you need anything else. 👍"
    elif any(kw in lowered for kw in bye_keywords):
        return "Goodbye! Take care. 👋"
    return None

# ============ Title ============
st.title("🎧 HarmoniChat: Emotion-Aware Music Chatbot")

persona = st.selectbox("Choose HarmoniChat's vibe/persona:", [
    "Friendly Bot 💖", "Calm Mentor 🧘", "Cheerful Motivator ☀️", "Romantic Companion 💌"
])

# ============ Session Init ============
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

user_input = ""

# ============ Voice / Text Input ============
if st.button("🎧 Use Voice Instead"):
    user_input = listen_to_voice()

user_input = st.text_input("Or type here:", user_input)

# ============ Main Logic ============
if user_input:
    short_reply = get_short_reply(user_input)

    if language_choice == "Hindi":
        translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)
        detected_lang = 'hi'
    else:
        translated_input = user_input
        detected_lang = 'en'

    emotion, score = detect_emotion(translated_input)

    if short_reply:
        gpt_reply = short_reply
    else:
        print("Before GPT4All")
        gpt_reply = generate_gpt4all_response(translated_input, emotion, st.session_state.chat_history, persona)
        
        
        print("After GPT4All")

    if detected_lang == 'hi':
        try:
            gpt_reply = GoogleTranslator(source='en', target='hi').translate(gpt_reply)
        except:
            pass

    log_mood(username, age, music_pref, emotion)

    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": gpt_reply})

    st.markdown(f"**🤖 HarmoniChat:** {gpt_reply}")
    if not short_reply:
        st.markdown(f"**🧠 Detected Emotion:** `{emotion.upper()}` ({score:.2f})")
        st.markdown(f"**🎵 Suggested Music:** [Click to Listen]({suggest_music(emotion)})")
    st.caption(f"🌍 Language: {language_choice}")

    speak_response(gpt_reply)

    st.markdown("---")
    st.markdown("### 📜 Chat History")
    for msg in st.session_state.chat_history:
        speaker = "🧑 You" if msg["role"] == "user" else "🤖 HarmoniChat"
        st.markdown(f"**{speaker}:** {msg['content']}")

    st.markdown("---")
    st.markdown("### 📊 Mood Tracker")
    history = get_mood_history(username)
    if history:
        timestamps, emotions = zip(*history)
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(timestamps, emotions, marker='o', linestyle='-', color='teal')
        ax.set_title(f"{username}'s Mood Trend")
        ax.set_xlabel("Time")
        ax.set_ylabel("Emotion")
        plt.xticks(rotation=45)
        st.pyplot(fig)

        warning = detect_low_mood_streak(history)
        if warning:
            st.warning(warning)
