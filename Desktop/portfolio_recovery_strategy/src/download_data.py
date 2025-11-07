import pandas as pd
import yfinance as yf
from .config import UNIVERSE, START, END

def fetch_daily(tickers=UNIVERSE, start=START, end=END):
    data = yf.download(tickers, start=start, end=end, auto_adjust=False, progress=False)
    # data columns: ('Adj Close','Close','High','Low','Open','Volume')
    if isinstance(data.columns, pd.MultiIndex):
        close = data["Close"].copy()
        vol = data["Volume"].copy()
    else:
        close = data["Close"].to_frame()
        vol = data["Volume"].to_frame()

    close = close.dropna(how="all")
    vol = vol.reindex_like(close)
    return close, vol

def to_weekly(close: pd.DataFrame, vol: pd.DataFrame):
    # Weekly Friday close; sum volume
    w_close = close.resample("W-FRI").last().dropna(how="all")
    w_vol = vol.resample("W-FRI").sum().reindex_like(w_close)
    return w_close, w_vol
