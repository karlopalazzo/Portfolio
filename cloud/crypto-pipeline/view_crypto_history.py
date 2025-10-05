from google.cloud import storage
import json
import matplotlib.pyplot as plt
from datetime import datetime

# Nazwa bucketu
BUCKET_NAME = "crypto-pipeline-data"

# Inicjalizacja klienta
client = storage.Client()
bucket = client.bucket(BUCKET_NAME)

# Pobranie wszystkich plików JSON
blobs = list(bucket.list_blobs())
blobs.sort(key=lambda b: b.name)  # sortowanie po nazwie (czas)

timestamps = []
btc_prices = []
eth_prices = []

for blob in blobs:
    data = json.loads(blob.download_as_text())
    # Wyciąganie cen
    btc = data.get("bitcoin", {}).get("usd")
    eth = data.get("ethereum", {}).get("usd")
    if btc is not None and eth is not None:
        # Wyciąganie timestampu z nazwy pliku: prices_2025-10-04T14-25-03.json
        ts_str = blob.name.replace("prices_", "").replace(".json", "")
        ts = datetime.strptime(ts_str, "%Y-%m-%dT%H-%M-%S")
        timestamps.append(ts)
        btc_prices.append(btc)
        eth_prices.append(eth)

# Wyświetlenie w terminalu
print("Ceny BTC i ETH:")
for t, btc, eth in zip(timestamps, btc_prices, eth_prices):
    print(f"{t}: BTC={btc}$, ETH={eth}$")

# Wykres
plt.figure(figsize=(10,5))
plt.plot(timestamps, btc_prices, label="Bitcoin (BTC)")
plt.plot(timestamps, eth_prices, label="Ethereum (ETH)")
plt.xlabel("Czas")
plt.ylabel("Cena USD")
plt.title("Historia cen BTC i ETH")
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()