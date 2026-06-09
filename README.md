# 🥷 Shadow Fight Arena — Gesture Automation System

> Hands-free combat automation for Shadow Fight Arena using real-time hand gesture recognition.

---

## 📹 Demo

[![▶ Watch Demo](https://img.shields.io/badge/▶%20Watch%20Demo-GitHub%20Video-black?style=for-the-badge&logo=github)](https://github.com/user-attachments/assets/9eba4848-2478-46fd-a3f2-cd8b6849ad23)

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
| Language | Python 3.x |

---

## 🎮 Gesture Mapping

| Gesture | In-Game Action |
|---|---|
| Open palm | Move forward |
| Closed fist | Block / defend |
| Swipe left | Dash left |
| Swipe right | Dash right |

---

## 🚀 Getting Started

### Prerequisites

```bash
pip install mediapipe opencv-python pyautogui
```

### Run

```bash
python basic.py
```

Make sure your webcam is connected and Shadow Fight Arena is open in a window. The script will auto-detect your hand and start mapping gestures to inputs.

---

## 🗂️ Project Structure

```
shadow-fight-automation/
├── basic.py                  # Entry point, main loop
├── gesture.py                # MediaPipe hand tracking + gesture classification
├── gesture_recognizer.task   # Pre-trained MediaPipe gesture model
└── README.md
```

---

## 🔧 Known Limitations

- Gesture detection accuracy can drop in low-light conditions
- Input simulation may lag on lower-end hardware
- Designed for PC/emulator gameplay; mobile not supported

---

## 👤 Author

**Anuj** — B.Tech CSE @ IIIT Bhopal  
Built as part of an exploration into computer vision and game automation.
