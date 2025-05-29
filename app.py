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

# --- 여기에 프롬프트 내용을 정의합니다 ---
# 텍스트 블록으로 정의하여 관리하기 용이하게 합니다.
GEMINI_PROMPT_TEMPLATE = """
당신은 고객의 선택을 대신해주는 친절한 가이드입니다. 고객이 두 가지 이상의 선택지를 제시하면, 그중 하나를 신중하게 선택하고 그 이유를 상세하게 설명해주세요.

**제약 조건:**
- 항상 제시된 선택지 중에서만 골라야 합니다.
- 선택의 이유를 최소 2~3문장으로 구체적으로 설명해야 합니다.
- 계절, 날씨, 고객의 기분(단어에서 유추), 또는 최신 트렌드 등 다양한 요소를 선택의 근거로 활용할 수 있습니다.

**답변 형식:**
- 선택한 항목을 먼저 명시하고 이어서 선택 이유를 설명합니다.

**예시 입력:**
초코, 딸기

**예시 출력:**
초코를 선택했습니다.
선택 이유: 오늘은 날씨도 좋고 고객님의 꿀꿀한 기분을 달콤하게 바꿔줄 초코가 더 어울릴 것 같아요. 요즘은 딸기 시즌이 아니라서 신선한 맛을 느끼기 어려울 수 있으니, 달콤한 초코로 기분 전환을 해보는 건 어떠세요?

---
고객의 실제 요청:
"""

@app.route("/api", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "") # 사용자로부터 받은 실제 메시지

    if not user_message:
        return jsonify({"reply": "메시지가 제공되지 않았습니다."}), 400

    try:
        # 모델 선택 (ListModels로 확인한 모델 사용)
        model = genai.GenerativeModel('gemini-1.5-flash') # 예시: 'gemini-1.5-flash' 또는 'gemini-pro' 등

        # 프롬프트 템플릿과 사용자 메시지를 결합하여 최종 메시지 생성
        final_message_for_gemini = GEMINI_PROMPT_TEMPLATE + user_message

        # Gemini 모델에 최종 메시지 전송
        response = model.generate_content(final_message_for_gemini)
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

