# app/firebase_connect.py
import firebase_admin
from firebase_admin import credentials, firestore
import os

service_account_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
cred = credentials.Certificate(service_account_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def save_analysis_to_firestore(user_id, original_text, analysis_result):
    """
    user_id: 사용자 ID (지금은 임시 UUID 가능)
    original_text: 유저 입력 대화 원문
    analysis_result: 감정 분석 결과 딕셔너리
    """
    from datetime import datetime
    from firebase_admin import firestore

    doc_ref = db.collection("users").document(user_id).collection("messages").document()

    doc_ref.set({
        "text": original_text,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "emotion_type": analysis_result.get("emotion_type"),
        "emotion_keywords": analysis_result.get("emotion_keywords", []),
        "gpt_reply": analysis_result.get("gpt_reply"),
        "reply_type": analysis_result.get("reply_type", "normal"),
        "is_input_insufficient": analysis_result.get("is_input_insufficient", False),
        "summary": analysis_result.get("summary", ""),
        "intent_to_continue": analysis_result.get("intent_to_continue", None),
        "partner_reaction": analysis_result.get("partner_reaction", ""),
    })

