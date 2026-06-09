# 🥷 Shadow Fight Arena — Gesture Automation System

> Hands-free combat automation for Shadow Fight Arena using real-time hand gesture recognition.

---

## 📹 Demo

https://github.com/user-attachments/assets/YOUR_VIDEO_ID_HERE

> **Note:** Replace the link above with your actual video URL (YouTube, Google Drive, or a GitHub-hosted `.mp4`). See [Adding Your Demo Video](#-adding-your-demo-video) below.

---

## 🧠 Overview

This project automates combat actions in **Shadow Fight Arena** by mapping real-time hand gestures (detected via webcam) to in-game keyboard/mouse inputs. No physical keyboard interaction is needed during gameplay — just move your hands.

Built in **February 2025** as a computer vision + automation side project.

---

## ⚙️ Tech Stack

| Component | Library |
|---|---|
| Hand Tracking | `MediaPipe` |
| Webcam Feed | `OpenCV` |
| Input Simulation | `PyAutoGUI` |
| Concurrency | `threading` |
| Language | Python 3.x |

---

## 🎮 Gesture Mapping

| Gesture | In-Game Action |
|---|---|
| Open palm | Move forward |
| Closed fist | Block / defend |
| Swipe left | Dash left |
| Swipe right | Dash right |

> Gesture mappings can be customized in `config.py`.

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install mediapipe opencv-python pyautogui
```

### Run

```bash
python main.py
```

Make sure your webcam is connected and Shadow Fight Arena is open in a window. The script will auto-detect your hand and start mapping gestures to inputs.

---

## 🗂️ Project Structure

```
shadow-fight-automation/
├── main.py              # Entry point, main loop
├── gesture_detector.py  # MediaPipe hand tracking + gesture classification
├── input_mapper.py      # Gesture → PyAutoGUI action mapping
├── config.py            # Configurable keybindings and thresholds
└── README.md
```

## 🔧 Known Limitations

- Gesture detection accuracy can drop in low-light conditions
- Input simulation may lag on lower-end hardware
- Designed for PC/emulator gameplay; mobile not supported

---

## 👤 Author

**Anuj** — B.Tech CSE @ IIIT Bhopal  
Built as part of an exploration into computer vision and game automation.

---

## 📄 License

MIT License — free to use, modify, and distribute.
