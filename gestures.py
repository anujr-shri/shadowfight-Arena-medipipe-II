import numpy as np
import keyboard
import time

sleep_time = 0.2

class GestureRecognizer:
    def __init__(self):
        self.current_movement_state = "center"
        self.is_holding = False
        self.last_strike_time = 0

        self.last_movement_detected_time = 0
        self.release_delay = 0.15  # Small buffer to prevent "double-tap" flicker

        self.initial_shoulder_y = None
        self.prev_wrist_coords = {"left": None, "right": None}

        self.strike_cooldown = 0.5
        self.JUMP_SENSITIVITY = 0.15
        self.TILT_SENSITIVITY = 0.18 
        self.PUNCH_VEL_SENSITIVITY = 0.05 
        self.PUNCH_ANGLE_REQ = 130

    def get_coords(self, landmarks, index):
        # MediaPipe landmarks have x, y, z
        lm = landmarks[index]
        return np.array([lm.x, lm.y, lm.z])

    def calculate_angle(self, a, b, c):
        ba = a - b
        bc = c - b
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        return np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))

    def detect_strike(self, landmarks, side="left"):
        # MediaPipe Indices: Left(11,13,15), Right(12,14,16)
        s_idx, e_idx, w_idx = (11, 13, 15) if side == "left" else (12, 14, 16)
        
        shoulder = self.get_coords(landmarks, s_idx)
        elbow = self.get_coords(landmarks, e_idx)
        wrist = self.get_coords(landmarks, w_idx)
        
        angle = self.calculate_angle(shoulder, elbow, wrist)
        
        # Velocity check
        current_wrist = wrist
        prev_wrist = self.prev_wrist_coords[side]
        vel = np.linalg.norm(current_wrist - prev_wrist) if prev_wrist is not None else 0
        self.prev_wrist_coords[side] = current_wrist  # type: ignore
        
        return angle > self.PUNCH_ANGLE_REQ and vel > self.PUNCH_VEL_SENSITIVITY

    def recognize_gesture(self, landmarks):
        curr_time = time.time()

        if self.detect_strike(landmarks, "left"):
            if (curr_time - self.last_strike_time) > self.strike_cooldown:
                self.last_strike_time = curr_time
                return "punch"
        elif self.detect_strike(landmarks, "right"):
            if (curr_time - self.last_strike_time) > self.strike_cooldown:
                self.last_strike_time = curr_time
                return "kick"

        l_sh = self.get_coords(landmarks, 11)
        r_sh = self.get_coords(landmarks, 12)
        avg_y = (l_sh[1] + r_sh[1]) / 2 

        if self.initial_shoulder_y is None:
            self.initial_shoulder_y = avg_y

        if (self.initial_shoulder_y - avg_y) > self.JUMP_SENSITIVITY:
            return "jump"
        
        if (r_sh[1] - l_sh[1]) > self.TILT_SENSITIVITY:
            return "tilt_left"
        elif (l_sh[1] - r_sh[1]) > self.TILT_SENSITIVITY:
            return "tilt_right"

        return "center"

    def execute_action(self, gesture):
        """Standard haaaa.py state logic for Shadow Fight 4"""
        now = time.time()
        
        action_map = {
            "tilt_left": 'A',
            "tilt_right": 'D',
            "jump": 'W',
            "punch": 'C',
            "kick": 'V'
        }

        # Determine current target
        target_movement = "center"
        if gesture == "tilt_left": target_movement = "left"
        elif gesture == "tilt_right": target_movement = "right"

        # 1. Update the timer if we are currently tilting
        if target_movement != "center":
            self.last_movement_detected_time = now

        
        effective_movement = target_movement
        if target_movement == "center" and self.is_holding:
            if (now - self.last_movement_detected_time) < self.release_delay:
                effective_movement = self.current_movement_state # Keep holding!

        # 3. STATE TRANSITION (The haaaa.py logic)
        if effective_movement != self.current_movement_state:
            # Release old
            if self.is_holding:
                old_key = action_map.get(f"tilt_{self.current_movement_state}")
                if old_key:
                    keyboard.release(old_key)
                    self.is_holding = False
            
            # Press new
            if effective_movement in ["left", "right"]:
                new_key = action_map[f"tilt_{effective_movement}"]
                keyboard.press(new_key)
                self.is_holding = True
            
            self.current_movement_state = effective_movement
        # 4. Instant actions (Taps)

        if gesture in ["punch", "kick", "jump"]:
            key = action_map.get(gesture)
            if key:
                keyboard.press_and_release(key)
        
        return action_map.get(gesture, "None")