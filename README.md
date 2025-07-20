# Virtual Gesture Keyboard

A real-time, hand-gesture-based virtual keyboard built with Python, OpenCV, and Mediapipe. It detects your index and thumb pinch to simulate key presses on a virtual keyboard rendered on the screen.

---

## ✨ Features

- Detects hand gestures using Mediapipe.
- Allows typing by pinching thumb and index finger over virtual keys.
- Automatically types into any active input field on screen using `pyautogui`.
- Recognizes Space, Enter, and Backspace keys.
- Closes the application when a fist is detected.

---

## 📦 Requirements

- Python 3.7+
- OpenCV
- Mediapipe
- PyAutoGUI

Install with:

```bash
pip install opencv-python mediapipe pyautogui
```

---

## 🚀 Usage
Run the script:

```bash
python virtual_keyboard.py
```
Then:
- Bring any input field (e.g., a text editor or browser input) into focus.
- Pinch your thumb and index finger on top of a virtual key to "press" it.
- Make a fist to exit the application.
