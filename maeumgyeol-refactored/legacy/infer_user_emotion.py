# app/infer_user_emotion.py

# app/infer_user_emotion.py

from openai import OpenAI

def analyze_user_emotion(user_lines, client: OpenAI = None) -> dict:
    """
    사용자의 발화를 바탕으로 감정 상태, 말투 성향, 관계 지속 의지를 추론한다.
    """
    if not user_lines:
        return {
            "감정 상태": "입력이 부족하여 분석 불가",
            "말투 성향": "-",
            "관계 지속 의지": "-",
            "해석 요약": "-"
        }

    prompt = f"""
    다음은 연애 대화에서 사용자의 발화 모음입니다:

    {chr(10).join(user_lines)}

    위 내용을 분석하여 다음 네 가지를 추론해주세요:
    1. 감정 상태 (한 문장 요약)
    2. 말투 성향 (예: 차분함, 다정함, 불안감 등)
    3. 관계 지속 의지 (예/아니오 + 이유)
    4. 전체 요약 해석 (두 문장 이내)

    형식:
    감정 상태: ...
    말투 성향: ...
    관계 지속 의지: ...
    해석 요약: ...
    """

    if client is None:
        raise ValueError("OpenAI client가 필요합니다.")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "너는 감정 분석 전문가야. 연애 대화에 특화된 분석을 제공해."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
    )

    output = response.choices[0].message.content.strip()

    # 결과 파싱
    lines = output.split("\n")
    result = {}
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip()

    return {
        "감정 상태": result.get("감정 상태", "-"),
        "말투 성향": result.get("말투 성향", "-"),
        "관계 지속 의지": result.get("관계 지속 의지", "-"),
        "해석 요약": result.get("해석 요약", "-")
    }

