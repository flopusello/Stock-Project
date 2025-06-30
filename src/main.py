from api.connectors import AlphaVantageClient
from processing.transformers import data_prep
from datetime import datetime
from file_management import (
    save_json_to_raw,
    load_json_from_processed,
    emptying_raw,
    emptying_processed,
)
from storage.mongo import insert_many, clean_collection

# Fill here the symbols of the stocks you want to track (limit to 25)

list = [
    "MSFT",  # Microsoft
    "NVDA",  # Nvidia
    "AAPL",  # Apple
    "AMZN",  # Amazon
    "META",  # Meta Platforms
    "AVGO",  # Broadcom
    "TSLA",  # Tesla
    "GOOGL",  # Alphabet Class A
    "BRK.B",  # Berkshire Hathaway Class B
    "GOOG",  # Alphabet Class C
    "JPM",  # JPMorgan Chase
    "V",  # Visa
    "LLY",  # Eli Lilly
    "NFLX",  # Netflix
    "COST",  # Costco
    "PG",  # Procter & Gamble
    "JNJ",  # Johnson & Johnson
    "HD",  # Home Depot
    "BAC",  # Bank of America
    "UNH",  # UnitedHealth Group
]

# Emptying Raw Data Folder

emptying_raw()

# Data Fetch

client = AlphaVantageClient()

for item in list:
    rows = []
    data = client.extract_daily(item)
    if not data:
        raise ValueError(f"Stock unavailable on Alpha Vantage: {item}")
    ts = data["Time Series (Daily)"]
    for date, metrics in ts.items():
        row = {
            "symbol": item,
            "date": date,
            "open": float(metrics["1. open"]),
            "high": float(metrics["2. high"]),
            "low": float(metrics["3. low"]),
            "close": float(metrics["4. close"]),
            "volume": int(metrics["5. volume"]),
        }
        rows.append(row)
    filename = f"{item}_{datetime.now().strftime('%Y%m%d')}_raw.json"
    save_json_to_raw(rows, filename)

# Emptying Processed Data Folder

emptying_processed()

# Processing of the data

for symbols in list:
    data_prep(symbols)

# Data Storage in MongoDB

clean_collection("stock_app", "stock_ts")

for symbols in list:
    data = load_json_from_processed(
        f"{symbols}_{datetime.now().strftime('%Y%m%d')}_processed.json"
    )
    for row in data:
        row["date"] = datetime.strptime(row["date"], "%Y-%m-%d")
    insert_many("stock_app", "stock_ts", data)

# End of the main script
