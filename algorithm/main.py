
import cv2
from algorithm.eye_detect import detect_eye_state

CLOSED_THRESHOLD = 30 #약 1초(30프레임) 동안 눈 감음 감지 시 졸음 경고

def main():
    print("프로그램 시작")
    cap = cv2.VideoCapture(0)  # 카메라 캡처 시작

    closed_frames = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break

        state = detect_eye_state(frame)

        if state == "CLOSED":
            closed_frames += 1
        else:
            closed_frames = 0

        if closed_frames >= CLOSED_THRESHOLD:
            drowsy_state = "DROWSY"
        else:
            drowsy_state = "AWAKE"

        print(f"눈 상태: {state}, 연속 감은 프레임: {closed_frames}, 졸음 상태: {drowsy_state}")

        cv2.imshow("Camera", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("프로그램 종료")

if __name__ == "__main__":
    main()