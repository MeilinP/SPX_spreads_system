from vix_condition import vix_condition
from trend_filter import trend_filter

def signal_engine(vix, spx_price, ma_200):
    vix_result = vix_condition(vix)
    trend_result = trend_filter(spx_price, ma_200)

    if not vix_result["trade"]:
        return {
            "trade": False,
            "reason": vix_result["reason"],
            "direction": None,
            "position_size": 0
        }

    return {
        "trade": True,
        "direction": trend_result["spread_direction"],
        "position_size": vix_result["multiplier"],
        "trend": trend_result["trend"]
    }

print(signal_engine(18, 5200, 5000))
print(signal_engine(28, 5200, 5000))
print(signal_engine(40, 5200, 5000))
print(signal_engine(18, 4800, 5000))