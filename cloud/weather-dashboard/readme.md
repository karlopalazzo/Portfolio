# Weather Dashboard

## Overview
Weather Dashboard is a cloud-based application deployed on Google Cloud Run. It periodically fetches real-time weather data from the OpenWeatherMap API and stores it in Google Cloud Storage. The application allows users to view the latest weather data in JSON format and can be extended to visualize it on a dashboard.

## Features
- Fetches weather data for a specified city using OpenWeatherMap API.
- Stores JSON data in Google Cloud Storage for persistence.
- Endpoints:
  - `/fetch` - Fetches the latest weather data and stores it in GCS.
  - `/weather` - (Optional) Can display or process stored weather data.
- Designed with DevOps principles in mind for easy deployment and scaling.

## Getting Started

### Prerequisites
- Google Cloud Project
- Google Cloud SDK installed
- OpenWeatherMap API key

### Environment Variables
Create a `.env` file in the project root:

```
OPENWEATHER_API_KEY=<your_openweather_api_key>
CITY_NAME=Warsaw
GCS_BUCKET_NAME=<your_gcs_bucket_name>
DATA_FOLDER=weather-data
```

### Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
pip install -r requirements.txt
```

### Running Locally
```bash
flask run
```
Endpoints:
- `http://localhost:8080/fetch` - fetch weather data
- `http://localhost:8080/weather` - view stored weather data

## Deployment
- Dockerized for Cloud Run deployment.
- Build and deploy using:

```bash
gcloud run deploy weather-dashboard --source . --region <region> --project <project_id>
```

## Project Structure
```
weather-dashboard/
├── app.py             # Main Flask app
├── Dockerfile
├── requirements.txt
├── .env               # Local environment variables (not committed)
└── weather-data/      # Folder where JSON files are stored
```

## License
MIT License
