import cv2
import mediapipe as mp
import pyautogui
import numpy as np

# Initialize MediaPipe Hand detection
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Screen size
screen_width, screen_height = pyautogui.size()

# Camera setup
cap = cv2.VideoCapture(0)

# Cursor smoothing variables
prev_x, prev_y = 0, 0
smooth_factor = 5  # Lower value = smoother movement

# Gesture tracking state
is_dragging = False

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read from camera.")
            break

        # Flip and preprocess the frame
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process frame with MediaPipe Hands
        result = hands.process(rgb_frame)
        landmarks = result.multi_hand_landmarks

        if landmarks:
            for hand_landmarks in landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Extract landmark positions
                lm_list = [(int(lm.x * frame_width), int(lm.y * frame_height)) for lm in hand_landmarks.landmark]

                # Get positions of required landmarks
                index_finger = lm_list[8]  # Index finger tip
                thumb_tip = lm_list[4]  # Thumb tip
                thumb_ip = lm_list[3]  # Thumb IP joint
                middle_finger = lm_list[12]  # Middle finger tip

                # Map index finger position to screen coordinates
                mapped_x = np.interp(index_finger[0], (0, frame_width), (0, screen_width))
                mapped_y = np.interp(index_finger[1], (0, frame_height), (0, screen_height))

                # Smooth cursor movement
                curr_x = prev_x + (mapped_x - prev_x) / smooth_factor
                curr_y = prev_y + (mapped_y - prev_y) / smooth_factor
                prev_x, prev_y = curr_x, curr_y

                # Gesture: Move Mouse
                pyautogui.moveTo(curr_x, curr_y)

                # Gesture: Drag (Pinch)
                distance_thumb_index = np.linalg.norm(np.array(thumb_tip) - np.array(index_finger))
                distance_thumb_ip = np.linalg.norm(np.array(thumb_ip) - np.array(thumb_tip))

                if distance_thumb_index < 40:  # Adjust threshold as needed
                    if not is_dragging:
                        pyautogui.mouseDown()
                        is_dragging = True
                else:
                    if is_dragging:
                        pyautogui.mouseUp()
                        is_dragging = False

                # Gesture: Left-Click
                if index_finger[1] < middle_finger[1]:  # Both index and middle fingers raised
                    pyautogui.click()

        # Display the frame
        cv2.imshow("Hand Gesture Controlled Mouse", frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    cap.release()
    cv2.destroyAllWindows()
