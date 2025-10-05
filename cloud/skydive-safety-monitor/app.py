from flask import Flask, request, jsonify
from google.cloud import storage
import os
import cv2
import numpy as np

app = Flask(__name__)

# ---- Konfiguracja ----
BUCKET_NAME = "skydive-video-storage"  # <- Twój bucket GCS
LOCAL_VIDEO_PATH = "/tmp"  # tymczasowy katalog w Cloud Run
MODEL_DIR = "models"
PROTOTXT = os.path.join(MODEL_DIR, "MobileNetSSD_deploy.prototxt")
MODEL = os.path.join(MODEL_DIR, "MobileNetSSD_deploy.caffemodel")
CLASSES = ["aeroplane", "person"]  # tylko te klasy

storage_client = storage.Client()

# ---- Endpoint root ----
@app.route("/", methods=["GET"])
def index():
    return "Skydive Safety Monitor is running!"

# ---- Lista wideo w bucketcie ----
@app.route("/videos", methods=["GET"])
def list_videos():
    bucket = storage_client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs(prefix="videos/")
    videos = [blob.name for blob in blobs if blob.name.endswith(".mp4")]
    return jsonify({"videos": videos})

# ---- Upload wideo ----
@app.route("/upload", methods=["POST"])
def upload_video():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    blob = storage_client.bucket(BUCKET_NAME).blob(f"videos/{file.filename}")
    blob.upload_from_file(file)
    return jsonify({"status": "success", "filename": file.filename})

# ---- Analiza i annotacja wideo ----
@app.route("/annotate/<video_name>", methods=["POST"])
def annotate_video(video_name):
    try:
        # Pobranie wideo z GCS
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"videos/{video_name}")
        local_path = os.path.join(LOCAL_VIDEO_PATH, video_name)
        blob.download_to_filename(local_path)

        # Sprawdzenie czy plik wideo istnieje
        if not os.path.exists(local_path):
            return jsonify({"error": f"Video {video_name} not found"}), 404

        # Wczytanie modelu
        net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)

        # Otworzenie wideo
        cap = cv2.VideoCapture(local_path)
        if not cap.isOpened():
            return jsonify({"error": f"Cannot open video {video_name}"}), 400

        # Przygotowanie do zapisu annotowanego wideo
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        annotated_path = os.path.join(LOCAL_VIDEO_PATH, f"annotated_{video_name}")
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(annotated_path, fourcc, fps, (width, height))

        frames_analyzed = 0
        detections_total = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Detekcja obiektów
            blob_input = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
            net.setInput(blob_input)
            detections = net.forward()

            for i in range(detections.shape[2]):
                confidence = detections[0, 0, i, 2]
                class_id = int(detections[0, 0, i, 1])
                if confidence > 0.5 and class_id < len(CLASSES):
                    label = CLASSES[class_id]
                    (h, w) = frame.shape[:2]
                    box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
                    cv2.putText(frame, label, (startX, startY - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    detections_total += 1

            out.write(frame)
            frames_analyzed += 1

        cap.release()
        out.release()

        # Upload annotowanego wideo do GCS
        annotated_blob = bucket.blob(f"analytics/annotated_{video_name}")
        annotated_blob.upload_from_filename(annotated_path)

        return jsonify({
            "status": "success",
            "video": video_name,
            "frames_analyzed": frames_analyzed,
            "detections_total": detections_total,
            "annotated_video": f"https://storage.googleapis.com/{BUCKET_NAME}/analytics/annotated_{video_name}"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
