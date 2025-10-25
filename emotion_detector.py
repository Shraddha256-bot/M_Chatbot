from transformers import pipeline

# Load emotion detection pipeline
emotion_classifier = pipeline("text-classification", 
                              model="bhadresh-savani/distilbert-base-uncased-emotion",
                              return_all_scores=True)

# Function to detect emotion
def detect_emotion(text):
    results = emotion_classifier(text)[0]
    results.sort(key=lambda x: x['score'], reverse=True)
    top_emotion = results[0]['label']
    confidence = results[0]['score']
    return top_emotion, confidence

# Mapping detected emotion to music link
def suggest_music(emotion_label):
    emotion_music_map = {
        'joy': "https://www.youtube.com/watch?v=Uy5VCOnqdAo&list=PL4sEAlydfKvst7zH_18G7MGJ-qYBB0o0h&index=3",
        'sadness': "https://www.youtube.com/watch?v=07DLCDhDfM8",
        'anger': "https://www.youtube.com/watch?v=2_BVk4AI4zI",
        'surprise': "https://www.youtube.com/watch?v=0oCwcZy4pVM",
        'disgust': "https://www.youtube.com/watch?v=QJO3ROT-A4E",
        'fear': "https://www.youtube.com/shorts/z2m8b8aMQtw",
        'neutral': "https://www.youtube.com/watch?v=EfcJevM_aWY",
        'love': "https://www.youtube.com/watch?v=tB8N3hzfCZo"
    }
    return emotion_music_map.get(emotion_label.lower(), "https://www.youtube.com/watch?v=DWcJFNfaw9c")


# Test
if __name__ == "__main__":
    user_input = input("Enter your message: ")
    emotion, score = detect_emotion(user_input)
    music_link = suggest_music(emotion)
    
    print(f"\nDetected Emotion: {emotion.upper()} ({score:.2f})")
    print(f"Suggested Music: {music_link}")

