import pandas as pd
import numpy as np

def rolling_high(s, window=260):
    return s.rolling(window, min_periods=1).max()

def build_index_signals(anchor_close_w, min_drop_weeks=4, cum_drop_pct=-0.08, recover_to=0.98):
    # anchor_close_w: pd.Series(index=Date, close)
    df = pd.DataFrame({"Close": anchor_close_w})
    df["RetW"] = df["Close"].pct_change()
    df["RollMax"] = rolling_high(df["Close"], 260)
    df["Drawdown"] = df["Close"] / df["RollMax"] - 1.0
    df["CumDropW"] = df["RetW"].rolling(min_drop_weeks, min_periods=1).sum()

    state = []
    mode = "FLAT"
    prior_high = np.nan

    for t, row in df.iterrows():
        c = row["Close"]
        dd = row["Drawdown"]
        cum = row["CumDropW"]

        trigger_reason = ""

        if mode in ("FLAT", "DELEVER"):
            # 触发建仓
            if (cum <= cum_drop_pct) or (dd <= cum_drop_pct):
                mode = "BUILD"
                prior_high = row["RollMax"]
                trigger_reason = "BUILD core"
        elif mode == "BUILD":
            # 进入运行期（下一周起执行 RUN 逻辑）
            mode = "RUN"
        elif mode == "RUN":
            # 反弹到前高附近 → 去杠杆
            if prior_high and (c >= prior_high * recover_to):
                mode = "DELEVER"
                trigger_reason = "DELEVER (recover)"

        state.append((t, mode, trigger_reason))

    sig = pd.DataFrame(state, columns=["Date","state","note"]).set_index("Date")
    return sig