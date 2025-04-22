import requests
from dotenv import load_dotenv
import os

load_dotenv()

url = "https://www.alphavantage.co/query"

params = {
    "apikey": os.getenv("av_api_key"),
    "function": "TIME_SERIES_DAILY",
    "symbol": "IBM",
}

response = requests.get(url, headers=None, params=params)
if response.status_code == 200:
    # Parse and print the JSON response data
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code} - {response.text}")
