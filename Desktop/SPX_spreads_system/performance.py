import pandas as pd
from backtest import results_df

total_days = len(results_df)
trade_days = results_df["trade"].sum()
no_trade_days = total_days - trade_days

direction_counts = results_df[results_df["trade"] == True]["direction"].value_counts()

vix_no_trade = results_df[results_df["trade"] == False]["reason"].value_counts()

print(f"总交易日: {total_days}")
print(f"产生信号天数: {trade_days} ({trade_days/total_days*100:.1f}%)")
print(f"不交易天数: {no_trade_days} ({no_trade_days/total_days*100:.1f}%)")
print(f"\n方向分布:")
print(direction_counts)
print(f"\n不交易原因:")
print(vix_no_trade)