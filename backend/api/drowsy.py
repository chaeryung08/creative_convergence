from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime
from storage.logger import log_drowsy_event

router = APIRouter()

#프론트엔드에서 보낼 데이터 형식
class DrowsyData(BaseModel):
    drowsy_level : float
    state:str
    user_id:str = "default_user"

#프론트엔드가 졸음상태 post로 전송함
@router.get("/drowsy")
def get_drowsy_status(data:DrowsyData):
    """
    졸음 상태를 계산해서 JSON으로 반환.
    - drowsy_level: 0 ~ 1 사이의 졸음 지수
    - state: NORMAL / WARNING / DROWSY
    - timestamp: 현재 시간
    """
    timestamp = datetime.now().isoformat()
  #프론트엔드에서측정한졸음상태를받아서저장

     # 로그 저장 (backend/storage/logger.py 사용)
    log_drowsy_event(
        timestamp=timestamp,
        drowsy_level=data.drowsy_level,
        state=data.state,
        user_id=data.user_id
    )
    
    # 응답
    return {
        "status": "success",
        "message": "졸음 데이터 저장 완료",
        "timestamp": timestamp,
        "received_data": {
            "drowsy_level": data.drowsy_level,
            "state": data.state
        }
    }
   
@router.get("/drowsy/logs")
def get_drowsy_logs():
    return{"message":"로그 조회 기능 (구현 필요)"}

