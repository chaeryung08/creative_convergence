from fastapi import APIRouter
from datetime import datetime
import random

router = APIRouter()

# 졸음 상태를 반환하는 API
@router.get("/drowsy")
def get_drowsy_status():
    """
    졸음 상태를 계산해서 JSON으로 반환.
    - drowsy_level: 0 ~ 1 사이의 졸음 지수
    - state: NORMAL / WARNING / DROWSY
    - timestamp: 현재 시간
    """
    # 예시: 랜덤으로 졸음 지수 생성
    drowsy_level = round(random.uniform(0, 1), 2)

    # 졸음 상태 판단
    if drowsy_level < 0.4:
        state = "NORMAL"
    elif drowsy_level < 0.7:
        state = "WARNING"
    else:
        state = "DROWSY"

    # JSON으로 반환
    return {
        "timestamp": datetime.now().isoformat(),
        "drowsy_level": drowsy_level,
        "state": state
    }
