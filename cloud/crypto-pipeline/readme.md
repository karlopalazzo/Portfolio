# Crypto Pipeline

Crypto Pipeline is a cloud-based Python application that fetches cryptocurrency prices periodically and stores the data in Google Cloud Storage.  
The project is designed to demonstrate building a cloud pipeline and working with scheduled tasks in GCP.

---

## Features

- Fetch cryptocurrency prices (BTC/USD and ETH/USD) from a public API
- Store JSON data in Google Cloud Storage
- Cloud Run deployment for scalable execution
- Integration with Cloud Scheduler for periodic data collection
- Simple API endpoint to trigger fetching manually

---

## Project Structure

crypto-pipeline/
├─ app.py            # main Python application code
├─ requirements.txt  # Python dependencies
├─ Dockerfile        # configuration for Cloud Run
├─ README.md
└─ data/             # folder for storing fetched JSON locally (optional)

---

## Requirements

- Python 3.10+
- Flask
- Requests
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

- **Fetch prices manually:**

POST /fetch

- **List latest prices stored:**

GET /prices

---

## Deployment to Google Cloud Run

1. Build and deploy the project:

gcloud run deploy crypto-pipeline --source . --region <REGION> --project <PROJECT_ID>

2. After deployment, you will get a link to the live cloud application.

---

## Future Improvements

- Add support for more cryptocurrencies
- Include historical data analysis and visualization
- Integration with dashboards or notifications

---

## Author

- Karol Palac (with assisstance of AI)
- Portfolio: https://github.com/karlopalazzo
