import pandas as pd
import yfinance as yf

def load_daily(tickers):
    data = yf.download(tickers, start="2016-01-01", auto_adjust=True, progress=False)
    # yfinance 多层列：('Close','AAPL') → 展开
    if isinstance(data.columns, pd.MultiIndex):
        data = data.swaplevel(axis=1).sort_index(axis=1)
    # 只留需要的
    wanted = ["Open","High","Low","Close","Volume"]
    frames = []
    for tk in tickers:
        if tk not in data.columns.levels[0]:
            continue
        df = data[tk][wanted].copy()
        df["Ticker"] = tk
        frames.append(df)
    out = pd.concat(frames).reset_index().rename(columns={"index":"Date"})
    out = out.set_index(["Ticker","Date"]).sort_index()
    return out

def to_weekly(ohlcv_multi):
    # 聚合为周线
    def agg_one(df):
        out = pd.DataFrame({
            "Open": df["Open"].resample("W-FRI").first(),
            "High": df["High"].resample("W-FRI").max(),
            "Low":  df["Low"].resample("W-FRI").min(),
            "Close":df["Close"].resample("W-FRI").last(),
            "Volume": df["Volume"].resample("W-FRI").sum(),
        })
        out["RetW"] = out["Close"].pct_change()
        return out

    weekly = []
    for tk in ohlcv_multi.index.get_level_values(0).unique():
        df = ohlcv_multi.loc[tk].copy()
        df.index = pd.to_datetime(df.index)
        w = agg_one(df)
        w["Ticker"] = tk
        weekly.append(w.reset_index().rename(columns={"index":"Date"}).set_index(["Ticker","Date"]))
    weekly = pd.concat(weekly).sort_index()

    # 透视成矩阵：周收益
    rets_w = weekly["RetW"].unstack(0)  # index=Date, columns=Ticker
    return weekly, rets_w