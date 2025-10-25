# 🎧 HarmoniChat — Emotion-Aware AI Music Chatbot

**HarmoniChat** is an intelligent, emotion-aware chatbot built with **Streamlit**, designed to understand your emotions, respond empathetically, and recommend music that matches your mood.

It’s not just a chatbot — it’s your emotional companion powered by AI 💬🎵

---

## 🌟 Features

✅ **Emotion Detection** — Analyzes text or voice to detect emotions using DistilBERT.  
🎤 **Voice Interaction** — Speak to HarmoniChat and get spoken replies via speech synthesis.  
🧠 **GPT Intelligence** — Generates empathetic, natural responses using GPT4All (offline) or OpenAI GPT (online).  
🎶 **Mood-Based Music Suggestions** — Suggests music from YouTube that aligns with your detected emotion.  
📊 **Mood Tracking Dashboard** — Logs your emotional patterns using SQLite and visualizes them with Matplotlib.  
🌍 **Multilingual Support** — Communicates in English and Hindi using `deep-translator`.  
🧘 **Customizable Personas** — Choose HarmoniChat’s personality (Friendly, Calm, Cheerful, or Romantic).

---

## 🧩 Tech Stack

| Category | Technology |
|-----------|-------------|
| **Frontend** | Streamlit |
| **Backend** | Python |
| **AI / NLP** | Transformers (DistilBERT Emotion Model) |
| **Database** | SQLite |
| **Speech & Audio** | SpeechRecognition, pyttsx3 |
| **Translation** | Deep Translator |
| **LLM Models** | GPT4All (local) / OpenAI GPT (API) |

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/HarmoniChat.git
cd HarmoniChat
