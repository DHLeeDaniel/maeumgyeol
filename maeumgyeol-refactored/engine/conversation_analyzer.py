from openai import OpenAI
import json

def analyze_conversation(conversation: str, client: OpenAI) -> dict:
    prompt = f"""
다음은 연인 간의 카톡 대화입니다:

[대화 내용]
{conversation}

이 대화를 기반으로 두 사람의 관계를 분석해줘. 결과는 다음 구조로 JSON 형식으로 반환해줘:

{{
  "관심도": "...",
  "말투 상황": "...",
  "대화 흐름": "...",
  "요약 해설": "...",
  "추천 멘트": "..."
}}

- 추천 멘트는 실제 채팅에서 쓸 수 있도록, 짧고 자연스럽고 감정이 담긴 한 문장으로 써줘.
- 말투는 부드럽고 진심 어린 톤. 너무 설명하지 말고, 마음을 전하는 말 한 줄만 써줘.
- 모든 항목을 반드시 채워서 JSON으로만 출력해줘.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return json.loads(response.choices[0].message.content)
# kyeol_infer.py

def infer_kyeol_types(text):
    # 예시로 단순 분류
    if any(word in text for word in ["고마워", "행복", "좋아해"]):
        return {
            "emotion_type": "Mireia",
            "emotion_keywords": ["감사", "애정", "행복"]
        }
    elif any(word in text for word in ["서운", "기다렸어", "왜 연락 안 해"]):
        return {
            "emotion_type": "Orphe",
            "emotion_keywords": ["기대", "불안", "서운함"]
        }
    else:
        return {
            "emotion_type": "Pro",
            "emotion_keywords": ["분석", "이성", "해결"]
        }
