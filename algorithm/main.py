
import cv2
from algorithm.eye_detect import detect_eye_state

def main():
    cap = cv2.VideoCapture(0)  # 카메라 캡처 시작

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        state = detect_eye_state(frame)
        print("눈 상태:", state)

        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
