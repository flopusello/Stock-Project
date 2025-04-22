from data.connectors import APIClient
from dotenv import load_dotenv
import os

load_dotenv()


class Extractor:
    def __init__(self):
        self.name = "Extractor"
        self.APIClient = APIClient()

    def extract(self, symbol):
        self.payload = {
            "apikey": os.getenv("av_api_key"),
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
        }

        data = self.APIClient.get_request(self.payload)

        return data


"""
rows = []
ts = data["Time Series (Daily)"]

for date, metrics in ts.items():
    row = {
        "symbol": symbol,
        "date": date,
        "open": float(metrics["1. open"]),
        "high": float(metrics["2. high"]),
        "low": float(metrics["3. low"]),
        "close": float(metrics["4. close"]),
        "volume": int(metrics["5. volume"]),
    }
    rows.append(row)
"""
