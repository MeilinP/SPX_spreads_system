import pandas as pd
import numpy as np

def apply_costs(we_w, cost_bp=5):
    """根据权重变化估算换手成本（双边≈权重变化的绝对值之和 * cost_bp）"""
    if cost_bp <= 0:
        return 0.0
    turn = we_w.diff().abs().sum(axis=1).fillna(0.0)  # 周度换手率
    # 将基点转成比例成本
    cost = turn * (cost_bp / 1e4)
    return cost

def backtest(rets_w, weights_w, cost_bp=5):
    rets_w = rets_w.copy().fillna(0.0)
    weights_w = weights_w.copy().fillna(0.0)

    # 列对齐
    common_cols = sorted(list(set(rets_w.columns) & set(weights_w.columns)))
    rets_w = rets_w[common_cols]
    weights_w = weights_w[common_cols]

    # 组合周收益（税前、费前）
    port_ret_raw = (weights_w * rets_w).sum(axis=1)

    # 费用
    cost_series = apply_costs(weights_w, cost_bp=cost_bp)

    port_ret = port_ret_raw - cost_series
    nav = (1.0 + port_ret).cumprod()
    nav.iloc[0] = 1.0  # 显式设定

    # 绩效指标
    ann = 52.0
    ret_mean = port_ret.mean()
    ret_std = port_ret.std()
    sharpe = (ret_mean / ret_std) * np.sqrt(ann) if ret_std > 0 else 0.0
    cagr = (nav.iloc[-1] ** (ann / len(nav)) - 1.0) if len(nav) > 0 else 0.0
    rollmax = nav.cummax()
    dd = nav / rollmax - 1.0
    maxdd = dd.min()

    stats = {
        "CAGR": float(cagr),
        "MaxDD": float(maxdd),
        "Vol": float(ret_std * np.sqrt(ann)),
        "Sharpe_0": float(sharpe),
    }

    equity = pd.DataFrame({
        "port_ret_raw": port_ret_raw,
        "cost": cost_series,
        "port_ret": port_ret,
        "nav": nav,
        "dd": dd
    })
    return equity, stats