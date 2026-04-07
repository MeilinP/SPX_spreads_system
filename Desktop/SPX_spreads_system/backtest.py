import yfinance as yf
import pandas as pd
from signal_engine import signal_engine

spx = yf.download("^GSPC", start="2020-01-01", end="2024-12-31", auto_adjust=True)["Close"].squeeze()
vix = yf.download("^VIX", start="2020-01-01", end="2024-12-31", auto_adjust=True)["Close"].squeeze()

df = pd.DataFrame({"spx": spx, "vix": vix})
df["ma_200"] = df["spx"].rolling(200).mean()
df = df.dropna()

results = []
for date, row in df.iterrows():
    signal = signal_engine(row["vix"], row["spx"], row["ma_200"])
    signal["date"] = date
    results.append(signal)

results_df = pd.DataFrame(results)
print(results_df[["date", "trade", "direction", "position_size"]].tail(20))