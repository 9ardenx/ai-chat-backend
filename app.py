import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai # Gemini SDK 임포트

app = Flask(__name__)
CORS(app)

# 환경 변수에서 API 키를 가져옵니다.
API_KEY = os.environ.get("GEMINI_API_KEY")

# API 키를 사용하여 Gemini SDK를 설정합니다.
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    print("경고: GEMINI_API_KEY 환경 변수가 설정되지 않았습니다.")

@app.route("/api", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")

    if not message:
        return jsonify({"reply": "메시지가 제공되지 않았습니다."}), 400

    try:
        # 'gemini-pro' 모델을 사용합니다.
        # chat-bison-001 대신 현재 사용 가능한 모델을 지정해야 합니다.
        # ListModels를 통해 다른 모델도 확인 가능합니다 (예: gemini-1.5-flash, gemini-1.5-pro)
        model = genai.GenerativeModel('gemini-pro')

        # generate_content 메서드를 사용하여 텍스트를 생성합니다.
        response = model.generate_content(message)

        # 응답 텍스트를 가져옵니다.
        reply = response.text

    except Exception as e:
        # API 호출 중 발생할 수 있는 에러를 처리합니다.
        # 예를 들어, API 키 오류, 할당량 초과 등이 있을 수 있습니다.
        reply = f"Gemini API 호출 중 에러 발생: {str(e)}"
        return jsonify({"reply": reply}), 500 # 500 Internal Server Error 반환

    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "Google Gemini API 연결 준비 완료! /api 엔드포인트로 POST 요청을 보내세요."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


