import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

thumb_ids = [1,2,3,4]

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand in results.multi_hand_landmarks:

            h, w, c = frame.shape
            puntos = []

            for id,lm in enumerate(hand.landmark):
                if id in thumb_ids:
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    puntos.append((cx,cy))

                    cv2.circle(frame,(cx,cy),7,(0,255,0),-1)

            if len(puntos)==4:
                cv2.line(frame,puntos[0],puntos[1],(0,255,0),3)
                cv2.line(frame,puntos[1],puntos[2],(0,255,0),3)
                cv2.line(frame,puntos[2],puntos[3],(0,255,0),3)

    cv2.imshow("Pulgares Detectados",frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
