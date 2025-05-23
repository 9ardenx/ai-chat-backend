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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render가 지정한 포트 사용
    app.run(host="0.0.0.0", port=port)        # 외부 접근 허용 + 포트 바인딩

