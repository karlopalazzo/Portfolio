# Skydive Safety Monitor

Skydive Safety Monitor is a cloud application for analyzing skydiving videos. The project uses Google Cloud Run and Google Cloud Storage to store and process videos in the cloud.

---

## Features

- Upload videos to the cloud (Google Cloud Storage)
- Video analysis to detect humans
- Annotate detected humans with bounding boxes
- API endpoints for managing videos and analysis results
- Optional integration with Cloud Scheduler for automatic video processing

---

## Project Structure

skydive-safety-monitor/
├─ app.py            # main Flask application code
├─ requirements.txt  # Python dependencies
├─ Dockerfile        # configuration for Cloud Run
├─ models/           # object detection models
└─ README.md

---

## Requirements

- Python 3.10+
- Flask
- OpenCV
- Google Cloud SDK
- Google Cloud Storage and Cloud Run (GCP project)

---

## Local Setup

1. Set up a virtual environment:

python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

2. Install dependencies:

pip install -r requirements.txt

3. Configure GCP access:

gcloud auth login
gcloud config set project <YOUR_PROJECT_ID>

4. Run the application locally:

python app.py

The application will be available at http://127.0.0.1:5000

---

## API Endpoints

- Upload video:

POST /upload

- List videos:

GET /videos

- Analyze / annotate video:

POST /annotate/<video_filename>

---

## Deployment to Google Cloud Run

1. Build and deploy the project:

gcloud run deploy skydive-safety-monitor --source . --region <REGION> --project <PROJECT_ID>

2. After deployment, you will get a link to the live cloud application.

---

## Future Improvements

- Improve accuracy of human detection in videos
- Detect risky behavior (e.g., collisions, close approaches)
- Integrate with a dashboard for visualization of results

---

## Author

- Karol Palac  (with AI assisstance)
- Portfolio: https://github.com/karlopalazzo
