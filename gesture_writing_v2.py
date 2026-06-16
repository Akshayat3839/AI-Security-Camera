import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# Camera
cap = cv2.VideoCapture(0)

# Canvas
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

prev_x, prev_y = 0, 0


def count_fingers(hand_landmarks):
    lm = hand_landmarks.landmark

    fingers = []

    # Thumb
    if lm[4].x < lm[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tips = [8, 12, 16, 20]
    bases = [6, 10, 14, 18]

    for tip, base in zip(tips, bases):
        if lm[tip].y < lm[base].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)


while True:

    success, frame = cap.read()

    if not success:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)


    mode = "PAUSE"

    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


            fingers = count_fingers(hand_landmarks)


            h, w, c = frame.shape

            index_tip = hand_landmarks.landmark[8]

            x = int(index_tip.x * w)
            y = int(index_tip.y * h)


            # 1 finger - Draw
            if fingers == 1:

                mode = "DRAW"

                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = x, y

                cv2.line(
                    canvas,
                    (prev_x, prev_y),
                    (x, y),
                    (0,255,0),
                    5
                )

                prev_x, prev_y = x, y


            # 2 fingers - Eraser
            elif fingers == 2:

                mode = "ERASER"

                cv2.circle(
                    canvas,
                    (x,y),
                    30,
                    (0,0,0),
                    -1
                )

                prev_x, prev_y = 0,0


            # 3 fingers - Save
            elif fingers == 3:

                mode = "SAVE"

                filename = (
                    "drawing_"
                    + datetime.now().strftime("%H%M%S")
                    + ".png"
                )

                cv2.imwrite(filename, canvas)

                prev_x, prev_y = 0,0


            else:

                prev_x, prev_y = 0,0



    output = cv2.add(frame, canvas)


    cv2.putText(
        output,
        "Mode: " + mode,
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )


    cv2.imshow(
        "AI Gesture Writing V2",
        output
    )


    key = cv2.waitKey(1)


    if key == ord('c'):

        canvas = np.zeros(
            (480,640,3),
            dtype=np.uint8
        )


    elif key == ord('q'):
        break



cap.release()
cv2.destroyAllWindows()