from openai import OpenAI

def extract_user_lines(conversation_text: str) -> str:
    user_lines = []
    for line in conversation_text.split("\n"):
        if line.strip().startswith("A:"):
            user_lines.append(line.replace("A:", "").strip())
    return "\n".join(user_lines)

def analyze_user_emotion(user_lines: str, client: OpenAI) -> dict:
    prompt = f"""
다음은 사용자(A)의 연애 대화 내용입니다:

{user_lines}

이 사용자의 감정 상태, 말투 성향, 관계 지속 의지를 감정적으로 분석해줘.
결과는 다음 형식으로 자연스럽게 정리해서 말해줘:

- 감정 상태:
- 말투 성향:
- 관계 지속 의지:
- 해석 요약:
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    result_text = response.choices[0].message.content.strip()

    # 딕셔너리 형태로 파싱
    result = {}
    for line in result_text.splitlines():
        if line.startswith("- ") and ":" in line:
            key, value = line[2:].split(":", 1)
            result[key.strip()] = value.strip()

    return result

