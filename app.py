#app.py


import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "maeumgyeol-refactored"))



import streamlit as st
from dotenv import load_dotenv
import os
from openai import OpenAI

# ⬇️ 리팩토링된 경로 기반 import
from engine.conversation_analyzer import analyze_conversation
from legacy.recovery_layer import clean_text
from engine.loop_detector import extract_user_lines
from legacy.infer_user_emotion import analyze_user_emotion
from pipeline import process_conversation_and_save

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from PIL import Image
import cv2
import numpy as np

import uuid

user_id = str(uuid.uuid4())[:8]  # 테스트용 임시 user_id

# 이미지 전처리 함수
def preprocess_image(pil_image):
    img = np.array(pil_image.convert("L"))
    _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
    return Image.fromarray(thresh)

# 환경 변수 로드 및 OpenAI 클라이언트 초기화
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# UI 시작
st.title("🧠 마음의결 maeumgyeol")
st.markdown("### 카톡 대화를 붙여넣으면, 상황을 분석하고 다음 대답을 추천해 드립니다.")

uploaded_file = st.file_uploader("📷 카톡 대화 캡처 업로드", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    original_image = Image.open(uploaded_file)
    image = preprocess_image(original_image)
    user_input = pytesseract.image_to_string(image, lang="kor+eng")
    st.text_area("🔍 OCR 추출 결과", value=user_input, height=150)
else:
    user_input = st.text_area("📱 카톡 대화 입력", height=200)

if st.button("분석 요청") and user_input.strip():
    with st.spinner("감정 및 관계 분석 중..."):
        try:
            cleaned = clean_text(user_input)

            # 사용자 감정 분석
            user_lines = extract_user_lines(user_input)
            emotion_summary = analyze_user_emotion(user_lines, client)

            st.markdown("### 🙋 사용자 감정 및 지속 의지 분석")
            st.markdown(f"""
            - **감정 상태**: {emotion_summary.get("감정 상태", "-")}
            - **말투 성향**: {emotion_summary.get("말투 성향", "-")}
            - **지속 의지**: {emotion_summary.get("관계 지속 의지", "-")}
            """)
            with st.expander("🔍 해석 요약 보기"):
                 st.write(emotion_summary.get("해석 요약", "-"))

            # 관계 분석 결과
            result = analyze_conversation(cleaned, client)
            st.markdown("### 💬 관계 분석 결과")
            st.markdown(f"""
            - **관심도**: {result.get("관심도", "-")}
            - **말투 상황**: {result.get("말투 상황", "-")}
            - **대화 흐름**: {result.get("대화 흐름", "-")}
            - **요약 해설**: {result.get("요약 해설", "-")}
            """)

            st.markdown("### 💌 추천 다음 대답")
            st.write(result.get("추천 멘트", "추천 멘트를 생성하지 못했습니다."))

            # 💡 GPT 기반 다음 대화 추천 (저장 포함)
            st.markdown("### 💡 GPT 기반 다음 대화 추천 (저장 포함)")
            gpt_reply, gpt_analysis_result = process_conversation_and_save(user_input, user_id)
            st.success(gpt_reply)

        except Exception as e:
            st.error(f"⚠️ 오류 발생: {e}")


