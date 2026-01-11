
import cv2
from algorithm.eye_detect import detect_eye_state
import time

def main():
    print("프로그램 시작")
    cap = cv2.VideoCapture(0)  # 카메라 캡처 시작

    fps = cap.get(cv2.CAP_PROP_FPS) # 카메라 FPS 가져오기
    if fps == 0:
        fps = 30  # 기본값 설정

    CLOSED_THRESHOLD = int(fps * 1.0)  # 약 1초(30프레임) 동안 눈 감음 감지 시 졸음 경고
    closed_frames = 0

    CALIBRATION_TIME = 5  # 보정 시간 (초)
    print(f"보정 중... {CALIBRATION_TIME}초 동안 눈을 감지 마세요.")
    ear_samples = []
    calibrated = False
    calibration_start = time.time()

    while True:
            ret, frame = cap.read()
            if not ret:
                print("프레임을 읽을 수 없습니다.")
                break

            state, ear = detect_eye_state(frame)
            current_time = time.time()

            # 보정 단계
            if not calibrated:
                cv2.putText(frame, "보정 중... 눈을 감지 마세요.",
                            (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.8, (0, 255, 255), 2)
            
                ear_samples.append(ear)

                if current_time - calibration_start >= CALIBRATION_TIME:
                    avg_ear = sum(ear_samples) / len(ear_samples)
                    EAR_THRESHOLD = avg_ear * 0.75  # 보정된 EAR 기준값 설정
                    calibrated = True
                    print("보정 완료")
                cv2.imshow("Drowsiness Detection", frame)
                if cv2.waitKey(1) & 0xFF == 27:  # ESC 키로 종료
                    break
                continue

            # 보정 완료 후 졸음 감지 단계
            if state == "CLOSED":
                closed_frames += 1
            else:
                closed_frames = 0

            if closed_frames >= CLOSED_THRESHOLD:
                drowsy_state = "DROWSY"
            else:
                drowsy_state = "AWAKE"

            print(f"눈 상태: {state}, 연속 감은 프레임: {closed_frames}, 졸음 상태: {drowsy_state}")

            cv2.imshow("Drowsiness Detection", frame)
            if cv2.waitKey(1) & 0xFF == 27: # ESC 키로 종료
                break

    cap.release()
    cv2.destroyAllWindows()
    print("프로그램 종료")

if __name__ == "__main__":
    main()