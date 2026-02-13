import numpy as np
import pydirectinput
import time

class GestureRecognizer:
    def __init__(self):
        self.previous_gesture = "none"
        self.last_action_time = 0
        self.cooldown = 0.5
        
        self.prev_wrist_coords = {"left": None, "right": None}
        self.initial_shoulder_y = None

        self.PUNCH_VEL_SENSITIVITY = 0.7  
        self.PUNCH_ANGLE_REQ = 130      
        self.JUMP_SENSITIVITY = 0.12    
        self.TILT_SENSITIVITY = 0.15     

    def get_coords(self, landmarks, index):
        lm = landmarks[index]
        return np.array([lm.x, lm.y, lm.z])

    def calculate_angle(self, a, b, c):
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        return np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

    def detect_strike(self, landmarks, side="left"):
        s_idx, e_idx, w_idx = (11, 13, 15) if side == "left" else (12, 14, 16)
        
        shoulder = self.get_coords(landmarks, s_idx)
        elbow = self.get_coords(landmarks, e_idx)
        wrist = self.get_coords(landmarks, w_idx)

        angle = self.calculate_angle(shoulder, elbow, wrist)
        
        current_wrist = wrist
        prev_wrist = self.prev_wrist_coords[side]
        vel = np.linalg.norm(current_wrist - prev_wrist) if prev_wrist is not None else 0
        self.prev_wrist_coords[side] = current_wrist # type: ignore
        
        return angle > self.PUNCH_ANGLE_REQ and vel > self.PUNCH_VEL_SENSITIVITY

    def recognize_gesture(self, landmarks):
        curr_time = time.time()
        current_gesture = "none"

        if self.detect_strike(landmarks, "left"):
            current_gesture = "punch"
        elif self.detect_strike(landmarks, "right"):
            current_gesture = "kick"
        
        else:
            l_sh = self.get_coords(landmarks, 11)
            r_sh = self.get_coords(landmarks, 12)
            avg_y = (l_sh[1] + r_sh[1]) / 2

            if self.initial_shoulder_y is None:
                self.initial_shoulder_y = avg_y

            if (l_sh[1] - r_sh[1]) > self.TILT_SENSITIVITY:
                current_gesture = "tilt_left"
            elif (r_sh[1] - l_sh[1]) > self.TILT_SENSITIVITY:
                current_gesture = "tilt_right"
            
            elif avg_y < (self.initial_shoulder_y - self.JUMP_SENSITIVITY):
                current_gesture = "up"

        
        if current_gesture != "none":
            if current_gesture != self.previous_gesture and (curr_time - self.last_action_time > self.cooldown):
                self.previous_gesture = current_gesture
                self.last_action_time = curr_time
                return current_gesture

        if current_gesture == "none":
            self.previous_gesture = "none"

        return "none"
def execute_game_action(gesture):
    """Map gestures to keyboard inputs for Shadow Fight Arena"""
    action_map = {
        "punch" : 'C',
        "kick" : 'V',
        "up" : 'W',
        "tilt_left" : 'A',
        "tilt_right" : 'D'
    }
    
    if gesture in action_map:
        pydirectinput.press(action_map[gesture])
        time.sleep(0.1)
        return action_map[gesture]
    return None
    

