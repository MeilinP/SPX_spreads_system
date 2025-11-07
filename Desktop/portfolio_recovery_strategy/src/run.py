import os
import pandas as pd
from .config import (TICKERS, ANCHOR, MIN_DROP_WEEKS, CUM_DROP_PCT, RECOVER_TO_PCT,
                     WEIGHTS_TEMPLATE, BUCKETS, COST_BP, RESULTS_DIR)
from .data import load_daily, to_weekly
from .signals import build_index_signals
from .portfolio import build_weight_matrix
from .backtest import backtest

def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print(f"Downloading daily data for: {TICKERS}")
    ohlc_d = load_daily(TICKERS)
    # 周线
    weekly, rets_w = to_weekly(ohlc_d)
    print(f"Weekly bars: {rets_w.index.min().date()} → {rets_w.index.max().date()}")

    # 指数信号（状态机）
    anchor_close = weekly.xs(ANCHOR, level=0)["Close"]
    sig = build_index_signals(
        anchor_close,
        min_drop_weeks=MIN_DROP_WEEKS,
        cum_drop_pct=CUM_DROP_PCT,
        recover_to=RECOVER_TO_PCT
    )

    # 打印关键 BUILD/DELEVER 事件
    for dt, row in sig.iterrows():
        if row["note"]:
            print(f"{dt.date()} {row['note']}")

    # 构建权重矩阵
    states = sig["state"]
    dates = sig.index
    weights_w = build_weight_matrix(dates, states, rets_w.columns.tolist(),
                                    WEIGHTS_TEMPLATE, BUCKETS)

    # 回测
    equity, stats = backtest(rets_w, weights_w, cost_bp=COST_BP)

    # 保存
    equity.to_csv(f"{RESULTS_DIR}/equity_curve.csv", index_label="Date")
    out_sig = sig.copy()
    out_sig.to_csv(f"{RESULTS_DIR}/index_signals.csv", index_label="Date")

    print("\n=== Performance ===")
    print(f"CAGR      : {stats['CAGR']*100:5.2f}%")
    print(f"MaxDD     : {stats['MaxDD']*100:5.2f}%")
    print(f"Vol       : {stats['Vol']*100:5.2f}%")
    print(f"Sharpe(0%): {stats['Sharpe_0']:5.2f}")
    print(f"Saved: {RESULTS_DIR}/equity_curve.csv, {RESULTS_DIR}/index_signals.csv")

if __name__ == "__main__":
    main()