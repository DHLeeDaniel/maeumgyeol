def style_output(result: str) -> str:
    lines = result.strip().split("\n")
    styled_lines = []
    for line in lines:
        if line.startswith("1. 관심도:"):
            styled_lines.append(f"**📌 관심도:** {line[6:].strip()}")
        elif line.startswith("2. 말투 성향:"):
            styled_lines.append(f"**🗣️ 말투 성향:** {line[7:].strip()}")
        elif line.startswith("3. 대화 흐름:"):
            styled_lines.append(f"**🔄 대화 흐름:** {line[7:].strip()}")
        elif line.startswith("4. 요약 분석:"):
            styled_lines.append(f"**🧠 요약 분석:** {line[7:].strip()}")
        elif line.startswith("5. 추천 멘트:"):
            styled_lines.append(f"**💬 추천 멘트:** {line[8:].strip()}")
    return "<br>".join(styled_lines)

