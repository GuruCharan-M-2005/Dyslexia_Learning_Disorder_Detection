import cv2
import dlib
import numpy as np
import base64
from flask import Flask, render_template, Response
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Load dlib's face detector and landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def get_eye_center(landmarks, eye_points):
    x = sum([landmarks.part(n).x for n in eye_points]) // 6
    y = sum([landmarks.part(n).y for n in eye_points]) // 6
    return (x, y)

@socketio.on('video_frame')
def process_frame(data):
    try:
        # Convert base64 to OpenCV image
        img_data = base64.b64decode(data.split(',')[1])
        np_img = np.frombuffer(img_data, dtype=np.uint8)
        frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)

        eye_positions = {}

        for face in faces:
            landmarks = predictor(gray, face)

            # Get left and right eye positions
            left_eye = np.array([[landmarks.part(n).x, landmarks.part(n).y] for n in range(36, 42)])
            right_eye = np.array([[landmarks.part(n).x, landmarks.part(n).y] for n in range(42, 48)])
            
            # Calculate center of eyes
            left_eye_center = np.mean(left_eye, axis=0).astype(int)
            right_eye_center = np.mean(right_eye, axis=0).astype(int)

            eye_positions = {
                "left_eye": [int(left_eye_center[0]), int(left_eye_center[1])],
                "right_eye": [int(right_eye_center[0]), int(right_eye_center[1])]
            }
            print("Detected eyes:",eye_positions)
            
        # Send eye positions back to frontend
        socketio.emit('eye_tracking_data', eye_positions)

    except Exception as e:
        print("Error processing frame:", e)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
