import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) 

def analyze_entry(entry_text):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')

        prompt = f"""
        Analyze this journal entry and provide insights about the person's emotional state, 
        potential patterns, and gentle suggestions for mental wellness:

        Entry: {entry_text}

        Please provide a supportive and constructive analysis.
        """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        return f"Error analyzing entry: {str(e)}"

def detect_mood(text):
    text = text.lower()
    if any(word in text for word in ["happy", "joy", "excited", "grateful"]):
        return "😊 Happy"
    elif any(word in text for word in ["sad", "depressed", "cry", "upset"]):
        return "😢 Sad"
    elif any(word in text for word in ["angry", "mad", "frustrated"]):
        return "😡 Angry"
    elif any(word in text for word in ["relaxed", "calm", "peaceful"]):
        return "😌 Calm"
    else:
        return "😐 Neutral"
