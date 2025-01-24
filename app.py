from transformers import pipeline
import random
import pandas as pd
from datetime import datetime
from flask import Flask, render_template, request

app = Flask(__name__)

feelings_analyzer = pipeline("sentiment-analysis")

def analyze_mood(user_input):
    result = feelings_analyzer(user_input)[0]
    mood = result['label']
    score = round(result['score'], 2)
    return mood, score

def generate_affirmation(mood):
    affirmations = {
        "POSITIVE": [
            "Your positive energy is inspiring—keep it going!",
            "Keep up the great work! You’re shining today!"
        ],
        "NEGATIVE": [
            "This moment will pass. You’re stronger than you think.",
            "Take it one step at a time; brighter days are ahead."
        ],
        "NEUTRAL": [
            "Today is a great day to focus on your goals. You've got this!",
            "Stay steady and remember—you’re doing better than you think!"
        ]
    }
    return random.choice(affirmations.get(mood, ["You're doing amazing"]))

def log_mood(user_input, mood, score):
    log_file = "mood_log.csv"
    current_date = datetime.now().strftime("%Y-%m-%d")
    new_entry = {"Date": current_date, "Input": user_input, "Mood": mood, "Score": score}

    try:
        df = pd.read_csv(log_file)
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    except FileNotFoundError:
        df = pd.DataFrame([new_entry])

    df.to_csv(log_file, index=False)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form.get("user_input")
        mood, score = analyze_mood(user_input)
        affirmation = generate_affirmation(mood)
        log_mood(user_input, mood, score)
        return render_template("index.html", mood=mood, score=score, affirmation=affirmation, user_input=user_input)
    return render_template("index.html")

@app.route("/test")
def test():
    return "Hello, I am alive!"

@app.route("/test-template")
def test_template():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")