import requests
from dotenv import load_dotenv
import os

load_dotenv()


class APIClient:
    def __init__(self):
        self.name = "API Client"

    def get_request(self, base_url, params: dict, headers=None):
        self.base_url = base_url
        self.params = params
        self.headers = headers
        response = requests.get(base_url, params=params, headers=headers)

        # Request Status Control
        if response.status_code == 200:
            data = response.json()

        else:
            print(f"Failed to retrieve data. Status code: {response.status_code}")
            print(response.text)
        return data


class AlphaVantageClient:
    def __init__(self):
        self.name = "Extractor"
        self.APIClient = APIClient()

    def extract_daily(self, symbol):
        self.base_url = "https://www.alphavantage.co/query"
        self.params = {
            "apikey": os.getenv("av_api_key"),
            "function": "TIME_SERIES_DAILY",
            "symbol": symbol,
        }

        data = self.APIClient.get_request(self.base_url, self.params)

        return data
