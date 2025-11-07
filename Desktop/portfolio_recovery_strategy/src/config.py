# 基本配置
TICKERS = [
    "SPY","QQQ","TQQQ","SPXL",
    "MSFT","GOOGL","AMZN","META",
    "GS","MS","IBKR","SCHW",
    "SPOT",
    "XOM","CVX","SLB","EPD",
    "UNH","AIG"
]

ANCHOR = "QQQ"   # 用于判定回撤/恢复的锚定指数

# 回撤-恢复信号参数（周频）
MIN_DROP_WEEKS = 4           # 连续弱势至少 N 周
CUM_DROP_PCT   = -0.08       # 近 N 周累计跌幅阈值
RECOVER_TO_PCT = 0.98        # 反弹到前高的 98% 视为“恢复”

# 组合权重模板
WEIGHTS_TEMPLATE = {
    "BUILD":   {"core":0.50, "platform":0.25, "lev":0.10, "energy":0.15},
    "DELEVER": {"core":0.55, "platform":0.30, "lev":0.00, "energy":0.15},
    "RUN":     None,  # 延续上一周权重（无大幅漂移则不调）
    "FLAT":    {"core":0.00, "platform":0.00, "lev":0.00, "energy":0.00},
}

# 分桶映射
BUCKETS = {
    "core":   ["SPY","QQQ"],
    "lev":    ["TQQQ","SPXL"],
    "platform": ["MSFT","GOOGL","AMZN","META","GS","MS","IBKR","SCHW","SPOT","AIG","UNH"],
    "energy": ["XOM","CVX","SLB","EPD"],
}

# 交易成本（基点，单边）
COST_BP = 5

RESULTS_DIR = "results"