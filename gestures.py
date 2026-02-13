import numpy as np
import pyautogui
import time

class GestureRecognizer:
    def __init__(self):
        self.previous_gesture = None
        self.gesture_threshold = 0.15
        self.last_action_time = 0
        self.cooldown = 0.3
        self.previous_wrist_positions = {"left": None, "right": None}
        
    def get_landmark_coords(self, landmarks, index):
        """Extract x, y, z coordinates of a landmark"""
        return landmarks[index].x, landmarks[index].y, landmarks[index].z
    
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points"""
        return np.sqrt((point1[0] - point2[0])**2 + 
                      (point1[1] - point2[1])**2 + 
                      (point1[2] - point2[2])**2)
    
    def left_punch(self, landmarks):
        """Detect Punch Gesture By Using the landmark position and their movement"""

        left_finger = self.get_landmark_coords(landmarks, index=20)
        left_shoulder = self.get_landmark_coords(landmarks, index=12)
        if left_finger == None or left_shoulder == None:
            return False
        arm_ext = False

        if left_finger[2] - left_shoulder[2] > 0.7:
            arm_ext = True
        return arm_ext
    
    def right_punch(self, landmarks):
        """Detect Punch Gesture By Using the landmark position and their movement"""
        right_finger = self.get_landmark_coords(landmarks, 19)
        right_shoulder = self.get_landmark_coords(landmarks, 11)
        arm_ext = False
        if right_finger[2] - right_shoulder[2] > 0.7:
            arm_ext = True
        return arm_ext

    def recognize_gesture(self, landmarks):
        if self.left_punch(landmarks):
            return "punch"
        if self.right_punch(landmarks):
            return "kick"
        return "none"
        
def execute_game_action(gesture):
    """Map gestures to keyboard inputs for Shadow Fight Arena"""
    action_map = {
        "punch_left": "j",
        "punch_right": "k",
        "kick_left": "u",
        "kick_right": "i",
        "block": "l", 
        "jump": "w",
        "crouch": "s", 
        "move_left": "a",
        "move_right": "d",
    }
    
    if gesture in action_map:
        pyautogui.press(action_map[gesture])
        return action_map[gesture]
    return None
    

