from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/api", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": message}]
    )

    return jsonify({"reply": response.choices[0].message["content"].strip()})

@app.route("/")
def home():
    return "AI 백엔드 작동 중!"
