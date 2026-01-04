from datetime import datetime, timedelta

# 알람 상태 관리용 전역 변수
alarm_counter = 0  # 최대 4번까지 알람
sleep_mode_locked = False  # 수면모드 제한 여부

def check_sleep_mode_allowed():
    """
    수면모드 사용 가능 여부 체크
    - 비수면 모드로 강제 이동했으면 수면모드 제한
    """
    return not sleep_mode_locked

def trigger_alarm():
    """
    알람/저주파기 시뮬레이션
    - 최대 4번 알람 후 잠자기 권유
    """
    global alarm_counter, sleep_mode_locked
    alarm_counter += 1

    if alarm_counter <= 4:
        # 알람 또는 저주파기 작동 시뮬레이션
        print(f"[{datetime.now().isoformat()}] 알람 {alarm_counter}번 작동")
        return {"alarm_triggered": True, "count": alarm_counter}
    else:
        # 최대 횟수 초과 → 수면 권유, 수면모드 제한
        sleep_mode_locked = True
        print(f"[{datetime.now().isoformat()}] 최대 알람 초과, 잠자기 권유")
        return {"alarm_triggered": False, "message": "잠자기 권유", "count": alarm_counter}

def reset_alarm():
    """
    알람 카운터 초기화 (새로운 세션 시작 등)
    """
    global alarm_counter, sleep_mode_locked
    alarm_counter = 0
    sleep_mode_locked = False
    print(f"[{datetime.now().isoformat()}] 알람 초기화 완료")
