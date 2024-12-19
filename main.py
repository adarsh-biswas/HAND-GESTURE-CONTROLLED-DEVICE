import cv2
import mediapipe as mp
import pyautogui
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)

screen_width, screen_height = pyautogui.size()
cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0
smooth_factor = 5
is_dragging = False

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from camera.")
            break

        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = hands.process(rgb_frame)
        landmarks = result.multi_hand_landmarks

        if landmarks:
            for hand_landmarks in landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                lm_list = [(int(lm.x * frame_width), int(lm.y * frame_height)) for lm in hand_landmarks.landmark]
                index_finger = lm_list[8]
                thumb_tip = lm_list[4]
                thumb_ip = lm_list[3]
                middle_finger = lm_list[12]
                mapped_x = np.interp(index_finger[0], (0, frame_width), (0, screen_width))
                mapped_y = np.interp(index_finger[1], (0, frame_height), (0, screen_height))
                curr_x = prev_x + (mapped_x - prev_x) / smooth_factor
                curr_y = prev_y + (mapped_y - prev_y) / smooth_factor
                prev_x, prev_y = curr_x, curr_y
                pyautogui.moveTo(curr_x, curr_y)
                distance_thumb_index = np.linalg.norm(np.array(thumb_tip) - np.array(index_finger))
                distance_thumb_ip = np.linalg.norm(np.array(thumb_ip) - np.array(thumb_tip))

                if distance_thumb_index < 40:
                    if not is_dragging:
                        pyautogui.mouseDown()
                        is_dragging = True
                else:
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False

                if index_finger[1] < middle_finger[1]:
                    pyautogui.click()

        cv2.imshow("Hand Gesture Controlled Mouse", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    cap.release()
    cv2.destroyAllWindows()
