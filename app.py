from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # 🔥 CORS 설정 추가

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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


