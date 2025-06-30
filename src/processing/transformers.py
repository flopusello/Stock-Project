import numpy as np
import pandas as pd
from datetime import datetime
from file_management import load_json_from_raw, save_json_to_processed


def data_prep(symbol):
    data = load_json_from_raw(f"{symbol}_{datetime.now().strftime('%Y%m%d')}_raw.json")
    if not data:
        raise ValueError(f"No data found for symbol: {symbol}")

    df = pd.DataFrame(data)
    df = df.sort_values("date", ascending=True)

    # Momentum Indicators

    for i in [9, 14, 20, 50]:
        df[f"SMA({i})"] = df["close"].rolling(window=i).mean()

    for i in [9, 12, 20, 26]:
        df[f"EMA({i})"] = df["close"].ewm(span=i, adjust=False).mean()

    df["gain"] = np.where(df["close"] > df["open"], df["close"] - df["open"], 0)

    df["loss"] = np.where(df["close"] < df["open"], df["open"] - df["close"], 0)

    df["avg_gain(14)"] = df["gain"].rolling(window=14).mean()
    df["avg_loss(14)"] = df["loss"].rolling(window=14).mean()

    df["rs(14)"] = df["avg_gain(14)"] / df["avg_loss(14)"]
    df["RSI(14)"] = 100 - (100 / (1 + df["rs(14)"]))

    df["MACD(12, 26)"] = df["EMA(12)"] - df["EMA(26)"]

    df["Signal Line(9)"] = df["MACD(12, 26)"].ewm(span=9, adjust=False).mean()

    # Volatility Indicators

    df["prev_close"] = df["close"].shift(1)
    df["tr1"] = df["high"] - df["low"]
    df["tr2"] = (df["high"] - df["prev_close"]).abs()
    df["tr3"] = (df["low"] - df["prev_close"]).abs()
    df["true_range"] = df[["tr1", "tr2", "tr3"]].max(axis=1)
    df["ATR(14)"] = df["true_range"].rolling(window=14).mean()
    df.drop(columns=["prev_close", "tr1", "tr2", "tr3", "true_range"], inplace=True)

    df["BB_upper(20, 2)"] = df["close"].rolling(window=20).mean() + (
        df["close"].rolling(window=20).std() * 2
    )

    df["BB_lower(20, 2)"] = df["close"].rolling(window=20).mean() - (
        df["close"].rolling(window=20).std() * 2
    )

    # Volume Indicators

    df["VWAP(14)"] = (df["close"] * df["volume"]).rolling(window=14).sum() / df[
        "volume"
    ].rolling(window=14).sum()

    df["OBV"] = (np.sign(df["close"].diff()) * df["volume"]).fillna(0).cumsum()

    df["Volume Spike(20)"] = (
        df["volume"] > df["volume"].rolling(window=20).mean() * 1.5
    ).astype(int)

    # Save Processed Data

    save_json_to_processed(
        df.to_dict(orient="records"),
        f"{symbol}_{datetime.now().strftime('%Y%m%d')}_processed.json",
    )
