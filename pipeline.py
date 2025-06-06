#pipeline.py

import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "maeumgyeol-refactored"))




from engine.conversation_analyzer import infer_kyeol_types
from legacy.recovery_layer import is_input_insufficient, get_recovery_prompt
from config.firebase_connect import save_analysis_to_firestore
from legacy.infer_partner_emotion import extract_partner_lines, analyze_partner_emotion

import openai
import uuid
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_conversation_and_save(user_text, user_id=None):
    if user_id is None:
        user_id = str(uuid.uuid4())[:8]

    # 사용자 감정 추론
    inferred = infer_kyeol_types(user_text)

    # 입력 부족한 경우
    if is_input_insufficient(user_text):
        gpt_reply = get_recovery_prompt()
        reply_type = "recovery"
    else:
        # GPT 응답 생성
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "너는 감정에 민감하고 다정한 연애 조언자야."},
                {"role": "user", "content": "이 대화 다음엔 어떤 말을 하면 좋을까?\n\n" + user_text}
            ],
            temperature=0.7,
        )
        gpt_reply = response.choices[0].message.content.strip()
        reply_type = "normal"

    # 🧠 상대방 감정 분석
    partner_lines = extract_partner_lines(user_text)
    partner_emotion = analyze_partner_emotion(partner_lines, openai)

    # 저장 데이터 구성
    analysis_result = {
        "emotion_type": inferred.get("emotion_type", ""),
        "emotion_keywords": inferred.get("emotion_keywords", []),
        "gpt_reply": gpt_reply,
        "reply_type": reply_type,
        "is_input_insufficient": is_input_insufficient(user_text),
        "partner_emotion": partner_emotion,
        "summary": "",
        "intent_to_continue": True,
        "partner_reaction": "",
    }

    save_analysis_to_firestore(user_id, user_text, analysis_result)

    return gpt_reply, analysis_result
