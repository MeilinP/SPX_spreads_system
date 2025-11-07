# =====================================================
# src/plot.py —— 生成展示级别图表 (兼容 Python 3.9)
# =====================================================
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = (12, 5)
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["font.size"] = 11

RESULT_DIR = "results"
EQ_PATH    = os.path.join(RESULT_DIR, "equity_curve.csv")
SIG_PATH   = os.path.join(RESULT_DIR, "index_signals.csv")

os.makedirs(RESULT_DIR, exist_ok=True)

def _read_equity_curve(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Could not find {path}")
    df = pd.read_csv(path)
    date_cols = [c for c in df.columns if c.lower() in ["date", "time", "datetime"]]
    date_col = date_cols[0] if date_cols else df.columns[0]
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col).set_index(date_col)

    candidates = ["equity", "nav", "cumret", "cum_return", "strategy", "portfolio", "value"]
    eq_col = None
    for c in df.columns:
        if c.lower() in candidates:
            eq_col = c
            break
    if eq_col is None:
        ret_cols = [c for c in df.columns if "ret" in c.lower()]
        if ret_cols:
            rc = ret_cols[0]
            df["equity"] = (1 + df[rc].fillna(0)).cumprod()
            eq_col = "equity"
        else:
            eq_col = df.columns[0]
    df["equity_norm"] = df[eq_col] / df[eq_col].iloc[0]
    return df[["equity_norm"]].rename(columns={"equity_norm": "Equity"})

def _read_signals(path):
    if not os.path.exists(path):
        print(f"[WARN] {path} not found. Signal lines will be skipped.")
        return None
    df = pd.read_csv(path)
    date_cols = [c for c in df.columns if c.lower() in ["date", "time", "week", "datetime"]]
    date_col = date_cols[0] if date_cols else df.columns[0]
    df[date_col] = pd.to_datetime(df[date_col])
    df = df.sort_values(date_col)
    df.rename(columns={date_col: "Date"}, inplace=True)

    if "event" in df.columns:
        event_col = "event"
    elif "signal" in df.columns:
        event_col = "signal"
    elif "state" in df.columns:
        event_col = "state"
    else:
        event_col = None
        build_col = next((c for c in df.columns if c.lower() == "build"), None)
        delever_col = next((c for c in df.columns if c.lower() in ["delever", "recover"]), None)
        if build_col or delever_col:
            df["event"] = np.where(build_col and df[build_col].astype(bool), "BUILD",
                            np.where(delever_col and df[delever_col].astype(bool), "DELEVER", ""))
            event_col = "event"

    if event_col is None:
        print("[WARN] No recognizable signal/event columns found.")
        return df[["Date"]].assign(event="")

    df[event_col] = df[event_col].astype(str)
    sig = df.loc[df[event_col].str.contains("BUILD|DELEVER", case=False, regex=True), ["Date", event_col]]
    sig.rename(columns={event_col: "event"}, inplace=True)
    return sig

def _plot_equity_with_signals(eq, sig, out_path):
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(eq.index, eq["Equity"], label="Strategy", linewidth=1.8)
    ax.set_title("Equity Curve")
    ax.set_ylabel("Normalized Equity (Start = 1.0)")
    ax.grid(alpha=0.3)

    if sig is not None and len(sig) > 0:
        for _, row in sig.iterrows():
            color = "#2ca02c" if "build" in row["event"].lower() else "#d62728"
            ax.axvline(row["Date"], color=color, alpha=0.25, linewidth=1.2)
        from matplotlib.lines import Line2D
        legend_lines = [
            Line2D([0], [0], color="#2ca02c", lw=2, label="BUILD"),
            Line2D([0], [0], color="#d62728", lw=2, label="DELEVER"),
        ]
        ax.legend(handles=[*ax.get_legend_handles_labels()[0], *legend_lines], loc="best")
    else:
        ax.legend(loc="best")

    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")

def _plot_underwater(eq, out_path):
    rolling_max = eq["Equity"].cummax()
    drawdown = eq["Equity"] / rolling_max - 1.0
    fig, ax = plt.subplots(figsize=(13, 3.8))
    ax.fill_between(eq.index, drawdown, 0, step="pre", alpha=0.6)
    ax.set_title("Underwater Curve (Drawdown)")
    ax.set_ylabel("Drawdown")
    ax.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")

def _plot_signals_timeline(sig, out_path):
    if sig is None or len(sig) == 0:
        print("[INFO] No signals to plot timeline. Skipped.")
        return
    fig, ax = plt.subplots(figsize=(13, 1.6))
    for _, row in sig.iterrows():
        color = "#2ca02c" if "build" in row["event"].lower() else "#d62728"
        ax.vlines(row["Date"], 0.1, 0.9, color=color, alpha=0.8)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.set_title("Signals Timeline (BUILD / DELEVER)")
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_path, dpi=200, bbox_inches="tight")
    plt.close()
    print(f"Saved: {out_path}")

def main():
    eq = _read_equity_curve(EQ_PATH)
    sig = _read_signals(SIG_PATH)
    _plot_equity_with_signals(eq, sig, os.path.join(RESULT_DIR, "equity_curve.png"))
    _plot_underwater(eq, os.path.join(RESULT_DIR, "underwater.png"))
    _plot_signals_timeline(sig, os.path.join(RESULT_DIR, "signals_timeline.png"))

if __name__ == "__main__":
    main()