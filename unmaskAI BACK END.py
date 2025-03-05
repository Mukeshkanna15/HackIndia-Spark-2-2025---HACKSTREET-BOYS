from flask import Flask, request, jsonify
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
from mtcnn import MTCNN

app = Flask(__name__)
model = load_model("models/xception_model.h5")
detector = MTCNN()
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return jsonify({"result": "No file uploaded"})

    video = request.files['video']
    video_path = os.path.join(UPLOAD_FOLDER, video.filename)
    video.save(video_path)

    result = process_video(video_path)
    return jsonify({"result": result})


def extract_faces(frame):
    faces = detector.detect_faces(frame)
    for face in faces:
        x, y, w, h = face['box']
        return frame[y:y+h, x:x+w]
    return None


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    predictions = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        face = extract_faces(frame)
        if face is not None:
            face = cv2.resize(face, (299, 299))
            face = face.astype("float32") / 255.0
            face = np.expand_dims(face, axis=0)
            prediction = model.predict(face)[0][0]
            predictions.append(prediction)
            frame_count += 1

        if frame_count >= 10:
            break

    cap.release()
    return "Fake" if np.mean(predictions) > 0.5 else "Real"

if __name__ == '__main__':
    app.run(debug=True)
