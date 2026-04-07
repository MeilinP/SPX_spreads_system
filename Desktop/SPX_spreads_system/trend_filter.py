def trend_filter(spx_price, ma_200):
    if spx_price > ma_200 * 1.01:
        return {"trend": "bullish", "spread_direction": "bull_put_spread"}
    elif spx_price < ma_200 * 0.99:
        return {"trend": "bearish", "spread_direction": "bear_call_spread"}
    else:
        return {"trend": "neutral", "spread_direction": "iron_condor"}
