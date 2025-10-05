from flask import Flask, jsonify
import requests
import os
from google.cloud import storage
from datetime import datetime
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
CITY_NAME = os.getenv("CITY_NAME", "Warsaw")
BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
DATA_FOLDER = "weather-data"

app = Flask(__name__)

# Initialize client GCS
storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)


@app.route("/fetch", methods=["GET"])
def fetch_weather():
    # Downloading data from OpenWeatherMap
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY_NAME}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch weather data"}), 500

    weather_data = response.json()

    # Preparing JSON file to be saved in GCS
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{DATA_FOLDER}/{CITY_NAME}_{timestamp}.json"

    blob = bucket.blob(filename)
    blob.upload_from_string(json.dumps(weather_data), content_type="application/json")

    return jsonify({
        "status": "success",
        "filename": filename,
        "data": weather_data
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
