import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("harmonichat.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mood_log (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        age INTEGER,
                        music_pref TEXT,
                        emotion TEXT,
                        timestamp TEXT
                    )''')
    conn.commit()
    conn.close()

def log_mood(username, age, music_pref, emotion):
    conn = sqlite3.connect("harmonichat.db")
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO mood_log (username, age, music_pref, emotion, timestamp) VALUES (?, ?, ?, ?, ?)",
                   (username, age, music_pref, emotion, now))
    conn.commit()
    conn.close()

def get_mood_history(username):
    conn = sqlite3.connect("harmonichat.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, emotion FROM mood_log WHERE username = ?", (username,))
    data = cursor.fetchall()
    conn.close()
    return data
