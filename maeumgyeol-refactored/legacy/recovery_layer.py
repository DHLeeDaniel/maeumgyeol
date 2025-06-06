import re

def clean_text(text):
    # 이모지, 특수기호 등 제거하고 공백 정리
    text = re.sub(r"[^\w\sㄱ-ㅎ가-힣.,!?~]", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip()

def is_input_insufficient(text):
    return len(text.strip()) < 10 or text.count("\n") < 1

def get_recovery_prompt():
    return "상대와 더 자연스럽게 대화를 이어가기 위한 상황을 설명해 주세요!"

