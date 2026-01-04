from fastapi import APIRouter
from core.alarm_logic import trigger_alarm, reset_alarm, check_sleep_mode_allowed

router = APIRouter(
    prefix="/alarm",
    tags=["alarm"]
)

@router.get("/trigger")
def alarm_trigger():
    """
    알람/저주파기 시뮬레이션 호출
    - 최대 4번 알람 후 잠자기 권유
    """
    if not check_sleep_mode_allowed():
        return {"status": "sleep_mode_locked", "message": "수면모드가 제한되어 알람 작동 불가"}
    
    result = trigger_alarm()
    return result

@router.get("/reset")
def alarm_reset():
    """
    알람 카운터 초기화
    """
    reset_alarm()
    return {"status": "reset", "message": "알람 초기화 완료"}
