from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class Request(BaseModel):
    message: str

# Our "Database" of study spots
def get_study_places():
    return [
        {"name": "Central Library", "type": "silent"},
        {"name": "Cafe Brew", "type": "moderate"},
        {"name": "City Study Hub", "type": "quiet"},
        {"name": "Green Park Pavilion", "type": "nature"}
    ]

def detect_mood(msg):
    msg = msg.lower()
    if any(word in msg for word in ["tired", "sleepy", "exhausted"]):
        return "idle"
    if any(word in msg for word in ["stress", "panic", "scared", "hard"]):
        return "panic"
    if any(word in msg for word in ["study", "exams", "grind", "work"]):
        return "grind"
    return "neutral"

@app.get("/")
def home():
    return {"status": "Buddy AI Agent is Online"}

@app.post("/agent")
def agent(req: Request):
    mood = detect_mood(req.message)
    places = get_study_places()
    
    # Logic: If panicked, suggest somewhere silent. Otherwise, pick random.
    if mood == "panic":
        suggestion = next(p for p in places if p["type"] == "silent")
    else:
        suggestion = random.choice(places)

    return {
        "reply": f"I noticed you're feeling {mood}. You should try {suggestion['name']}.",
        "mood": mood,
        "place_type": suggestion["type"],
        "agent": "Buddy AI MCP"
    }