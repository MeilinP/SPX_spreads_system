def vix_condition(vix):
    if vix < 15:
        return {"trade": False, "multiplier": 0, "reason": "VIX too low, premium not worth it"}
    elif vix <= 25:
        return {"trade": True, "multiplier": 1.0, "reason": "Normal environment"}
    elif vix <= 35:
        return {"trade": True, "multiplier": 0.5, "reason": "High volatility, half size"}
    else:
        return {"trade": False, "multiplier": 0, "reason": "Extreme volatility, no trade"}
