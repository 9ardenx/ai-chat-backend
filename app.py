import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/api", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent?key={API_KEY}"
        headers = {"Content-Type": "application/json"}
        body = {
            "contents": [
                {
                    "parts": [{"text": message}]
                }
            ]
        }

        res = requests.post(url, headers=headers, json=body)
        res_json = res.json()

        # ✅ 에러 응답 처리
        if "error" in res_json:
            return jsonify({"reply": f"Gemini API 오류: {res_json['error']['message']}"})

        # ✅ 정상 응답 처리
        reply = res_json["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        reply = f"에러 발생: {str(e)}"

    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "Gemini API 직접 호출 중!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

