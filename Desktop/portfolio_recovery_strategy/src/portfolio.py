import pandas as pd

def _bucket_of(ticker, buckets):
    for b, names in buckets.items():
        if ticker in names:
            return b
    return None

def target_weights_for_state(state, template, tickers, buckets):
    # RUN: 不主动调（由上周延续），返回 None
    if state == "RUN":
        return None

    alloc = template[state]
    # 展开到每个资产（等权分配到分桶内）
    w = {tk: 0.0 for tk in tickers}
    for bucket, portion in alloc.items():
        members = [tk for tk in tickers if _bucket_of(tk, buckets) == bucket]
        if members and portion > 0:
            sub = portion / len(members)
            for tk in members:
                w[tk] = sub
    return pd.Series(w, name="weight")

def build_weight_matrix(dates, states, tickers, template, buckets, rebal_tol=0.02):
    """
    按周生成权重矩阵；RUN 状态延续上一周；无持仓显式 0。
    """
    W = []
    last_w = None
    for dt, st in states.items():
        tw = target_weights_for_state(st, template, tickers, buckets)
        if tw is None:
            # RUN: 延续
            if last_w is None:
                tw = target_weights_for_state("FLAT", template, tickers, buckets)
            else:
                tw = last_w.copy()
        tw.name = dt
        # 归一化（避免浮点误差）
        s = tw.sum()
        if s > 0:
            tw = tw / s
        else:
            tw = tw.fillna(0.0)
        W.append(tw)
        last_w = tw
    W = pd.DataFrame(W, index=dates)
    W = W.reindex(index=dates, columns=tickers, fill_value=0.0)
    return W