import cv2
import mediapipe as mp
import pyautogui
import time

# Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # width
cap.set(4, 720)   # height

# Updated Keyboard Layout (Numbers + QWERTY + Special Keys)
keys = [
    ['1','2','3','4','5','6','7','8','9','0'],
    ['Q','W','E','R','T','Y','U','I','O','P'],
    ['A','S','D','F','G','H','J','K','L',],
    ['Z','X','C','V','B','N','M'],
    ['Space', 'Enter', 'Backspace']
]

# Store typed text
typed_text = ""
last_press_time = 0

# Draw the virtual keyboard
def draw_keyboard(img):
    key_boxes = []
    x_start, y_start = 50, 100
    key_h = 80
    
    for row_idx, row in enumerate(keys):
        for col_idx, key in enumerate(row):
            if key in ['Space', 'Enter', 'Backspace']:
                key_w = 220   
            else:
                 key_w = 80
            x = x_start + col_idx * (key_w + 10)
            y = y_start + row_idx * (key_h + 10)
            # Increase width for special keys
            
            key_boxes.append((key, (x, y, key_w, key_h)))

            cv2.rectangle(img, (x, y), (x + key_w, y + key_h), (255, 0, 255), 2)
            text_size = cv2.getTextSize(key, cv2.FONT_HERSHEY_SIMPLEX, 1.3, 2)[0]
            text_x = x + (key_w - text_size[0]) // 2
            text_y = y + (key_h + text_size[1]) // 2
            cv2.putText(img, key, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,0,0), 2)

    return key_boxes

# Check if hand is closed (fist)
def is_fist_closed(landmarks):
    tips = [8, 12, 16, 20]  # fingertips
    folded = 0
    for tip in tips:
        if landmarks[tip].y > landmarks[tip - 2].y:
            folded += 1
    return folded >= 4  # All fingers (except thumb) folded

# Main loop
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    key_boxes = draw_keyboard(img)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            h, w, c = img.shape
            lm = handLms.landmark

            # Get index fingertip position
            x_tip = int(lm[8].x * w)
            y_tip = int(lm[8].y * h)
            cv2.circle(img, (x_tip, y_tip), 10, (0, 255, 0), cv2.FILLED)

            # Check for each key hit
            # Check distance between thumb tip (4) and index fingertip (8)
            thumb_tip = lm[4]
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            cv2.circle(img, (thumb_x, thumb_y), 10, (0, 255, 0), cv2.FILLED)
            distance = ((thumb_x - x_tip)**2 + (thumb_y - y_tip)**2)**0.5

            # Only proceed if thumb and index finger tips are very close (pinch gesture)
            if distance < 40:  # you can tweak this threshold
                for key, (x, y, w_, h_) in key_boxes:
                    if x < x_tip < x + w_ and y < y_tip < y + h_:

                        cv2.rectangle(img, (x, y), (x + w_, y + h_), (0,255,0), cv2.FILLED)
                        cv2.putText(img, key, (x+10, y+50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0,0,0), 2)

                        if time.time() - last_press_time > 1:
                            if key == "Space":
                                typed_text += " "
                                pyautogui.press("space")
                            elif key == "Enter":
                                typed_text += "\n"
                                pyautogui.press("enter")
                            elif key == "Backspace":
                                typed_text = typed_text[:-1]
                                pyautogui.press("backspace")
                            else:
                                typed_text += key
                                pyautogui.press(key.lower())
                            last_press_time = time.time()

                # If fist is closed, quit
                if is_fist_closed(lm):
                    print("Fist detected, exiting...")
                    cv2.putText(img, "FIST DETECTED - EXITING", (50, 650), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                    cv2.imshow("Virtual Keyboard", img)
                    cv2.waitKey(1000)
                    cap.release()
                    cv2.destroyAllWindows()
                    exit()

     # Draw typed text on screen
    cv2.putText(img, f"Typed: {typed_text}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3)
    cv2.imshow("Virtual Keyboard", img)
    if cv2.waitKey(1) == 27:  # ESC to exit manually
            break

cap.release()
cv2.destroyAllWindows()