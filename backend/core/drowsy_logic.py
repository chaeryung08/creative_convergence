# core/drowsy_logic.py

def 판단하기(drowsy_level: float):
    # 졸음 수치가 0.8 이상이면 위험 상태
    if drowsy_level >= 0.8:
        return "WARNING"
    # 0.5 이상이면 주의
    elif drowsy_level >= 0.5:
        return "CAUTION"
    # 그 외는 정상
    else:
        return "NORMAL"
