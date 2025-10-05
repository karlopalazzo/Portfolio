import json
import io
import datetime
import requests
from flask import Flask, jsonify, Response
from google.cloud import storage
import matplotlib.pyplot as plt

app = Flask(__name__)

BUCKET_NAME = "crypto-pipeline-data"

@app.route("/")
def home():
    return "✅ Crypto Pipeline is running. Use /fetch or /chart."


@app.route("/fetch")
def fetch_prices():
    """Fetch current crypto prices and store as JSON in GCS."""
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {"ids": "bitcoin,ethereum,cardano", "vs_currencies": "usd"}
    r = requests.get(url, params=params)
    data = r.json()
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"crypto_prices_{timestamp}.json"

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(json.dumps(data))
    return jsonify({"status": "success", "file": filename, "data": data})


@app.route("/chart")
def chart():
    """Generate a matplotlib chart from JSON files in GCS."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blobs = list(bucket.list_blobs())

    timestamps = []
    prices_btc = []
    prices_eth = []
    prices_ada = []

    for blob in sorted(blobs, key=lambda b: b.name):
        if blob.name.endswith(".json"):
            content = json.loads(blob.download_as_text())
            timestamps.append(blob.name.replace("crypto_prices_", "").replace(".json", ""))
            prices_btc.append(content.get("bitcoin", {}).get("usd", 0))
            prices_eth.append(content.get("ethereum", {}).get("usd", 0))
            prices_ada.append(content.get("cardano", {}).get("usd", 0))

    if not timestamps:
        return jsonify({"error": "No JSON data found in bucket"})

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, prices_btc, label="Bitcoin (USD)")
    plt.plot(timestamps, prices_eth, label="Ethereum (USD)")
    plt.plot(timestamps, prices_ada, label="Cardano (USD)")
    plt.legend()
    plt.title("Crypto Prices Over Time")
    plt.xticks(rotation=45)
    plt.tight_layout()

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png")
    plt.close()
    img_bytes.seek(0)

    return Response(img_bytes.getvalue(), mimetype="image/png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)