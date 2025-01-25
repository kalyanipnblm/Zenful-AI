from flask import Flask, render_template, request
from flask.cli import load_dotenv
import os
import openai

load_dotenv()
app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_response(user_input):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a friendly and empathetic assistant. Respond naturally as if you are a supportive friend that really wants to help and provide the best advice. "
                        "Provide inspirational responses that feel personal and conversational. Avoid overly formal or robotic language. "
                        "At the end, provide an inspirational quote that is related to the user input to make the user feel better."
                    ),
                },
                {
                    "role": "user",
                    "content": f"{user_input}"
                }
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"


@app.route("/", methods=["GET", "POST"])
def home():
    mood_response = None
    if request.method == "POST":
        user_input = request.form.get("user_input")
        if user_input:
            mood_response = generate_response(user_input)
    return render_template("index.html", mood_response=mood_response)

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
