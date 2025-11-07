# 📈 Portfolio Recovery Strategy

**Goal:**  
A long-term **portfolio recovery & compounding strategy** designed to buy during multi-week drawdowns and deleverage during recoveries — aligning with cyclical accumulation behavior of U.S. equity markets.

---

## 🧭 Strategy Overview

This strategy follows a **two-phase cycle**:

| Phase | Condition | Action |
|-------|------------|--------|
| 🟢 **BUILD** | Weekly cumulative drawdown ≥ -8% and ≥ 4 consecutive red weeks | Increase exposure: core index (SPY, QQQ), leading "moat" companies, + small leverage leg (SPXL / TQQQ). |
| 🔴 **DELEVER (Recover)** | Index rebound ≥ +6% from local low | Deleverage / trim ETF exposure, keep quality stocks for long-term holding. |

This reflects the principle that *most major U.S. equity drawdowns revert within several months*, and *quality monopolistic sectors tend to recover faster than broad indices.*

---

## ⚙️ Portfolio Composition

| Bucket | Allocation | Description |
|---------|-------------|-------------|
| **Core Index Exposure** | 50% | SPY / QQQ – long-term base. |
| **Moat / “Dealer” Stocks** | 25% | Financials, Cloud, Ads, Data Services, IP-heavy firms (GOOGL, META, AMZN, MSFT, IBKR, GS, SPOT, etc.). |
| **Hard Assets / Energy** | 15% | Oil, Gas, Mining, Energy Transport (XOM, CVX, SLB, EPD). |
| **Leveraged ETF (TQQQ/SPXL)** | 10% | Tactical boost during deep drawdowns only. |

---

## 📊 Backtest Summary (2016–2025)

| Metric | Value |
|:-------|------:|
| **CAGR** | 12.41% |
| **Max Drawdown** | -38.46% |
| **Annualized Volatility** | 20.09% |
| **Sharpe Ratio (0%)** | 0.68 |

---

## 📈 Visual Results

### Equity Curve
![Equity Curve](results/equity_curve.png)

### Drawdown Curve
![Underwater Curve](results/underwater.png)

### Signal Timeline
![Signals Timeline](results/signals_timeline.png)

---

## 🔍 Key Observations

- The model alternates between **“BUILD core”** and **“DELEVER (recover)”** periods, roughly every 6–12 months.
- Deep drawdowns (COVID 2020, 2022 bear market) generated strong re-entry opportunities.
- Limiting leveraged ETF exposure (≤5%) significantly reduces MaxDD while keeping CAGR >10%.

---

## 🚀 Next Steps

Planned improvements:
1. Add **conditional leverage activation** (e.g., only if VIX > 25 and RSI < 40).  
2. Introduce **soft stop-loss logic** during extended “U-shape” recoveries.  
3. Backtest across global indices (e.g., STOXX50, HSI) for robustness.

---

**Author:** Meilin Pan  
**Updated:** November 2025  
📂 Files generated:  
`results/equity_curve.csv` · `results/index_signals.csv` · plots in `/results/`