from datetime import datetime
from typing import Dict, Optional
import requests

# API 엔드포인트 설정
API_BASE_URL = 'http://localhost:5000/api'  # 백엔드 서버 주소
USE_MOCK_DATA = True  # True: Mock 모드, False: API 연동 모드

# Mock 졸음 데이터
mock_sleep_data = {
    'user_id': 'user_001',
    'current_status': 'drowsy',
    'drowsiness_level': 75,
    'eye_closure_rate': 0.65,
    'last_update': datetime.now().isoformat(),
}

# 졸음 상태 레벨 정의
drowsiness_levels = {
    'alert': {
        'level': 'alert',
        'label': '정상',
        'color': '#4CAF50',
        'range': (0, 25),
        'emoji': '😊',
    },
    'drowsy': {
        'level': 'drowsy',
        'label': '졸림',
        'color': '#FFC107',
        'range': (26, 50),
        'emoji': '😴',
    },
    'very_drowsy': {
        'level': 'very_drowsy',
        'label': '매우 졸림',
        'color': '#FF9800',
        'range': (51, 75),
        'emoji': '😪',
    },
    'sleeping': {
        'level': 'sleeping',
        'label': '수면 중',
        'color': '#F44336',
        'range': (76, 100),
        'emoji': '💤',
    },
}

def get_drowsiness_level(score: int) -> Dict:
    """졸음 레벨 판단 함수"""
    if score <= 25:
        return drowsiness_levels['alert']
    elif score <= 50:
        return drowsiness_levels['drowsy']
    elif score <= 75:
        return drowsiness_levels['very_drowsy']
    else:
        return drowsiness_levels['sleeping']


# ===== API 통신 함수들 =====

def fetch_drowsiness_status() -> Dict:
    """백엔드에서 현재 졸음 상태 가져오기"""
    if USE_MOCK_DATA:
        print("[Mock Mode] Mock 데이터 사용 중")
        return mock_sleep_data.copy()
    
    try:
        response = requests.get(f'{API_BASE_URL}/drowsiness', timeout=3)
        response.raise_for_status()
        data = response.json()
        
        return {
            'user_id': data.get('user_id', 'user_001'),
            'current_status': data.get('current_status', 'alert'),
            'drowsiness_level': data.get('drowsiness_level', 0),
            'eye_closure_rate': data.get('eye_closure_rate', 0.0),
            'last_update': data.get('last_update', datetime.now().isoformat()),
        }
    except Exception as e:
        print(f"[API Error] 백엔드 연결 실패, Mock 데이터 사용: {e}")
        return mock_sleep_data.copy()


def set_alarm_api(alarm_time: str) -> Dict:
    """알람 설정 API 호출"""
    if USE_MOCK_DATA:
        print(f"[Mock Mode] 알람 설정: {alarm_time}")
        return {'success': True, 'message': 'Mock 알람 설정 완료'}
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/alarm',
            json={'alarm_time': alarm_time, 'enabled': True},
            timeout=3
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[API Error] 알람 설정 실패: {e}")
        return {'success': False, 'error': str(e)}


def cancel_alarm_api() -> Dict:
    """알람 취소 API 호출"""
    if USE_MOCK_DATA:
        print("[Mock Mode] 알람 취소")
        return {'success': True, 'message': 'Mock 알람 취소 완료'}
    
    try:
        response = requests.delete(f'{API_BASE_URL}/alarm', timeout=3)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[API Error] 알람 취소 실패: {e}")
        return {'success': False, 'error': str(e)}


def send_event_log_api(event_type: str, data: Dict) -> Dict:
    """이벤트 로그를 백엔드에 전송"""
    if USE_MOCK_DATA:
        return {'success': True}
    
    try:
        response = requests.post(
            f'{API_BASE_URL}/logs',
            json={
                'event_type': event_type,
                'data': data,
                'timestamp': datetime.now().isoformat()
            },
            timeout=3
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[API Error] 로그 전송 실패: {e}")
        return {'success': False, 'error': str(e)}
USE_MOCK_DATA = True  # Mock 모드 활성화

