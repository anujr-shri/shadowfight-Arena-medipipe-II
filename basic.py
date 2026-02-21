import numpy as np
import mediapipe as mp
from mediapipe.tasks.python.vision import drawing_utils, PoseLandmarker
from mediapipe.tasks.python.vision import drawing_styles, PoseLandmarkerOptions, RunningMode
from mediapipe.tasks.python import vision
from mediapipe.tasks import python
import cv2
import time
from gestures import GestureRecognizer

def draw_landmarks_on_image(detection_result, rgb_image):
    """Draws pose landmarks and connections on the image."""
    pose_landmarks_list = detection_result.pose_landmarks
    annotated_image = np.copy(rgb_image)
    pose_landmark_style = drawing_styles.get_default_pose_landmarks_style()
    pose_connection_style = drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2)

    for pose_landmarks in pose_landmarks_list:
        drawing_utils.draw_landmarks(
            image=annotated_image,
            landmark_list=pose_landmarks,
            connections=vision.PoseLandmarksConnections.POSE_LANDMARKS,
            landmark_drawing_spec=pose_landmark_style,
            connection_drawing_spec=pose_connection_style)

    return annotated_image


def main():
    frame_count = 0
    base_option = python.BaseOptions(
        model_asset_path="pose_landmarker_full.task", # Ensure this file is in your folder
        delegate=mp.tasks.BaseOptions.Delegate.CPU
    )

    option = PoseLandmarkerOptions(
        base_options=base_option,
        running_mode=RunningMode.VIDEO, # Required for video file/stream processing
        num_poses=1,
    )

    # Initialize the Recognizer (This maintains the state/memory)
    gesture_recognizer = GestureRecognizer()

    # Create detector and start camera
    with PoseLandmarker.create_from_options(option) as detector:
        cap = cv2.VideoCapture(0)
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        print("Controller Active. Press 'q' to quit.")

        while cap.isOpened():
            success, img = cap.read()
            if not success:
                break

            img = cv2.flip(img, 1) # Flip for mirror effect
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            mp_img = mp.Image(data=rgb_img, image_format=mp.ImageFormat.SRGB)
            
            timestamp_ms = int(time.time() * 1000) 
            result = detector.detect_for_video(mp_img, timestamp_ms)
            
            # 3. Draw landmarks for visual feedback
            annotated_img = draw_landmarks_on_image(result, mp_img.numpy_view())
            
            # Variables for UI display
            current_gesture = "center"
            active_key = "None"
            
            if result.pose_landmarks:
                # result.pose_landmarks is a list of normalized landmarks
                landmarks = result.pose_landmarks[0]
                
                # Identify the gesture based on landmark indices (11-16)
                current_gesture = gesture_recognizer.recognize_gesture(landmarks)
                
                # Execute action using the instance's internal state memory
                active_key = gesture_recognizer.execute_action(current_gesture)
            
            # 5. UI Overlay
            # Convert back to BGR for OpenCV display
            display_img = cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR)
            
            cv2.putText(display_img, f"Gesture: {current_gesture}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.putText(display_img, f"Active Key: {active_key}", (10, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            cv2.imshow('Shadow Fight 4 Controller', display_img)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()