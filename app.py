import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GEMINI_API_KEY")

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
        # 여기에 ListModels로 확인된 정확한 모델 이름을 입력하세요!
        # 예를 들어 'models/gemini-1.5-flash' 또는 'models/gemini-1.5-pro'
        # 'gemini-pro'가 계속 오류가 난다면 다른 모델을 사용해야 합니다.
        model = genai.GenerativeModel('gemini-1.5-flash') # <-- 이 부분을 변경!

        response = model.generate_content(message)
        reply = response.text

    except Exception as e:
        reply = f"Gemini API 호출 중 에러 발생: {str(e)}"
        print(f"에러 상세: {e}")
        return jsonify({"reply": reply}), 500

    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "Google Gemini API 백엔드 연결 준비 완료! `/api` 엔드포인트로 POST 요청을 보내세요."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

