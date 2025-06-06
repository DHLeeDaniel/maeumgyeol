# infer_partner_emotion.py

import re
import openai

# 사용자 ID 기준으로 발화 주체 구분 (예: "A: ...", "B: ...")
def extract_partner_lines(conversation_text: str, user_id: str = "A") -> list:
    pattern = re.compile(rf"{user_id}:\s?(.*?)\n")
    all_lines = re.findall(r"(A|B):\s?(.*?)\n?", conversation_text)
    partner_lines = [line for speaker, line in all_lines if speaker != user_id]
    return partner_lines

# GPT를 통해 상대방 감정 분석
def analyze_partner_emotion(partner_lines: list, openai_client) -> dict:
    joined_text = "\n".join(partner_lines)
    prompt = f"""
다음은 상대방의 대화 내용입니다. 이 사람이 어떤 감정을 느끼고 있고, 말투 성향은 어떤지, 그리고 관계를 지속하고 싶은 의지가 있는지를 분석해 주세요.

상대방 대사:
{joined_text}

응답 형식 예시:
- 감정 상태: ...
- 말투 성향: ...
- 관계 지속 의지: ...
- 해석 요약: ...
"""
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return parse_emotion_response(response.choices[0].message.content)

# GPT 결과 텍스트를 딕셔너리로 파싱
def parse_emotion_response(response_text: str) -> dict:
    lines = response_text.strip().split("\n")
    result = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()
    return result

# 관계 유지 의지 점수화 (간단한 기준)
def score_partner_intent(emotion_result: dict) -> float:
    intent = emotion_result.get("관계 지속 의지", "")
    if "있음" in intent:
        return 0.9
    elif "명확하지 않음" in intent or "불확실" in intent:
        return 0.5
    elif "없음" in intent or "부정" in intent:
        return 0.1
    return 0.0
