# partner_analysis.py

from typing import List, Dict
import re

def extract_partner_statements(dialogue: str) -> List[str]:
    """
    A, B 등 대화자 중 상대방(B)의 발화를 추출한다.
    """
    pattern = r"(?:^|\n)[Bb]:\s*(.*)"
    return re.findall(pattern, dialogue)

def analyze_partner_emotion(lines: List[str]) -> Dict[str, str]:
    """
    간단한 감정 분석 예시 (키워드 기반)
    - 향후 GPT 통합 또는 ML 모델 연동 가능
    """
    emotion = "중립"
    keywords = {
        "긍정": ["좋아", "고마워", "괜찮아", "행복", "예쁘다"],
        "부정": ["싫어", "짜증", "화나", "귀찮아", "힘들어", "무서워"],
    }

    full_text = " ".join(lines)
    for key, words in keywords.items():
        if any(word in full_text for word in words):
            emotion = key
            break

    return {
        "partner_emotion": emotion,
        "partner_lines": lines
    }

def infer_partner_emotion(dialogue: str) -> Dict[str, str]:
    """
    전체 파이프라인: 대화에서 상대방(B)의 발화를 추출하고 감정 분석
    """
    partner_lines = extract_partner_statements(dialogue)
    return analyze_partner_emotion(partner_lines)
