from flask import Flask, render_template, request
import openai

app = Flask(__name__)

openai.api_key = "sk-your-api-key-here"

def generate_response(user_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that analyzes mood and provides positive affirmations."},
                {"role": "user", "content": f"Analyze the mood of this input and provide a positive affirmation:\n\n{user_input}"}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
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
