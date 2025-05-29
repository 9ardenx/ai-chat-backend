from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# 환경변수에서 키 불러오기
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Gemini 설정
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/text-bison-001")

@app.route("/api", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    try:
        response = model.generate_content(message)
        reply = response.text.strip()
    except Exception as e:
        reply = f"에러 발생: {str(e)}"

    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "Gemini 백엔드 작동 중!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


