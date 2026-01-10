from datetime import datetime
from typing import Dict, List, Any
import json

class EventLogger:
    """이벤트 로거 - 앱 내 모든 이벤트 기록"""
    
    def __init__(self):
        self.logs: List[Dict] = []
        self.max_logs = 100  # 최대 로그 개수
    
    def log(self, event_type: str, data: Dict[str, Any] = None) -> Dict:
        """이벤트 로그 추가"""
        if data is None:
            data = {}
            
        log_entry = {
            'id': int(datetime.now().timestamp() * 1000),
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'data': data,
        }
        
        self.logs.insert(0, log_entry)
        
        # 최대 로그 개수 초과 시 오래된 로그 삭제
        if len(self.logs) > self.max_logs:
            self.logs = self.logs[:self.max_logs]
        
        print(f"[Event Log] {event_type}: {data}")
        return log_entry
    
    def log_timer_start(self, duration: int) -> Dict:
        """타이머 시작 로그"""
        return self.log('TIMER_START', {'duration': duration})
    
    def log_timer_stop(self, remaining_time: int) -> Dict:
        """타이머 정지 로그"""
        return self.log('TIMER_STOP', {'remaining_time': remaining_time})
    
    def log_alarm_set(self, time: str) -> Dict:
        """알람 설정 로그"""
        return self.log('ALARM_SET', {'time': time})
    
    def log_alarm_cancel(self) -> Dict:
        """알람 취소 로그"""
        return self.log('ALARM_CANCEL', {})
    
    def log_drowsiness_change(self, old_level: str, new_level: str, score: int) -> Dict:
        """졸음 상태 변경 로그"""
        return self.log('DROWSINESS_CHANGE', {
            'old_level': old_level,
            'new_level': new_level,
            'score': score
        })
    
    def log_screen_enter(self, screen_name: str) -> Dict:
        """화면 진입 로그"""
        return self.log('SCREEN_ENTER', {'screen_name': screen_name})
    
    def get_all_logs(self) -> List[Dict]:
        """모든 로그 가져오기"""
        return self.logs
    
    def get_logs_by_type(self, event_type: str) -> List[Dict]:
        """특정 타입 로그만 가져오기"""
        return [log for log in self.logs if log['event_type'] == event_type]
    
    def clear_logs(self):
        """로그 초기화"""
        self.logs = []
        self.log('LOGS_CLEARED', {})

# 싱글톤 인스턴스 생성
event_logger = EventLogger()