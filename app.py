from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# 최신 방식의 OpenAI 클라이언트
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/api", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # ✅ 여기!
    messages=[{"role": "user", "content": message}]
)

    return jsonify({"reply": response.choices[0].message.content.strip()})

@app.route("/")
def home():
    return "AI 백엔드 작동 중!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


