from algorithm.eye_detect import detect_eye_state

def main():
    print("프로그램 시작")

    closed_count = 0
    THRESHOLD = 3  # 눈 감긴 프레임 수 임계값

    for i in range(5):  # 예시로 5프레임 처리
        dummy_frame = None #나중에 카메라 프레임으로 교체
        state = detect_eye_state(dummy_frame)

        print(f"{i+1}번째 프레임 눈 상태:", state)

        if state == "CLOSED":
            closed_count += 1
        else:
            closed_count = 0

        if closed_count >= THRESHOLD:
            print("졸음 상태 감지")
            break

    print("프로그램 종료")

if __name__ == "__main__":
    main()
