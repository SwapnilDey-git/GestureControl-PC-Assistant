import cv2
import mediapipe as mp
from pynput.keyboard import Controller, Key
import time
import threading
import tkinter as tk

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize Keyboard
keyboard = Controller()

# Variables
running = False
cooldown = 1.0  # seconds

def gesture_control():
    global running

    cap = cv2.VideoCapture(0)
    prev_time = 0
    last_action_time = 0

    while running:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        frame_height, frame_width, _ = frame.shape
        mid_x = frame_width // 2

        # Draw center line
        cv2.line(frame, (mid_x, 0), (mid_x, frame_height), (0, 255, 0), 2)

        current_time = time.time()

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            # Tip of Index and Middle fingers
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

            index_x = int(index_tip.x * frame_width)
            middle_x = int(middle_tip.x * frame_width)

            # Draw circles
            cv2.circle(frame, (index_x, int(index_tip.y * frame_height)), 10, (255, 0, 255), -1)
            cv2.circle(frame, (middle_x, int(middle_tip.y * frame_height)), 10, (255, 0, 255), -1)

            if current_time - last_action_time > cooldown:
                if index_x < mid_x and middle_x < mid_x:
                    print("Move LEFT ⬅️")
                    keyboard.press(Key.ctrl_l)
                    keyboard.press(Key.shift_l)
                    keyboard.press(Key.tab)
                    keyboard.release(Key.tab)
                    keyboard.release(Key.shift_l)
                    keyboard.release(Key.ctrl_l)
                    last_action_time = current_time

                elif index_x > mid_x and middle_x > mid_x:
                    print("Move RIGHT ➡️")
                    keyboard.press(Key.ctrl_l)
                    keyboard.press(Key.tab)
                    keyboard.release(Key.tab)
                    keyboard.release(Key.ctrl_l)
                    last_action_time = current_time

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Display FPS
        fps = 1 / (current_time - prev_time) if current_time != prev_time else 0
        prev_time = current_time
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        cv2.imshow("Gesture Control", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Functions to start/stop
def start_gesture():
    global running
    if not running:
        running = True
        threading.Thread(target=gesture_control).start()

def stop_gesture():
    global running
    running = False

# GUI using Tkinter
root = tk.Tk()
root.title("Gesture Control Panel")
root.geometry("300x200")

start_button = tk.Button(root, text="Start Control", command=start_gesture, font=("Arial", 14), bg="green", fg="white")
start_button.pack(pady=20)

stop_button = tk.Button(root, text="Stop Control", command=stop_gesture, font=("Arial", 14), bg="red", fg="white")
stop_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.destroy, font=("Arial", 12))
exit_button.pack(pady=10)

root.mainloop()
