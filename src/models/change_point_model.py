import os
import sys
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 📦 Set path for imports from src/
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.append(SRC_DIR)

def clean_dates(date_str):
    if isinstance(date_str, str):
        return re.sub(r"[^\w\s\-:/]", "", date_str.strip())
    return date_str

def parse_dates_safely(date_series):
    # 🔍 Inspect sample values to guess format
    sample = date_series.dropna().astype(str).iloc[:50].tolist()
    formats = ["%d-%b-%y", "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"]
    for fmt in formats:
        try:
            pd.to_datetime(sample, format=fmt)
            return pd.to_datetime(date_series, format=fmt, errors="coerce")
        except Exception:
            continue
    return pd.to_datetime(date_series, errors="coerce")

def preprocess_brent_data():
    df = pd.read_csv("data/raw/BrentOilPrices.csv")
    df["Date"] = df["Date"].apply(clean_dates)
    df["Date"] = parse_dates_safely(df["Date"])
    df.dropna(subset=["Date", "Price"], inplace=True)
    df["LogReturn"] = np.log(df["Price"]).diff()
    df.dropna(subset=["LogReturn"], inplace=True)
    return df

def run_changepoint_detector():
    df = preprocess_brent_data()
    df = df.tail(1500)
    log_returns = df["LogReturn"].values

    def split_likelihood(t):
        r1, r2 = log_returns[:t], log_returns[t:]
        mu1, mu2 = np.mean(r1), np.mean(r2)
        s1, s2 = np.std(r1) + 1e-6, np.std(r2) + 1e-6
        ll1 = -np.sum((r1 - mu1)**2) / (2 * s1**2)
        ll2 = -np.sum((r2 - mu2)**2) / (2 * s2**2)
        return ll1 + ll2

    scores = [split_likelihood(t) for t in range(30, len(log_returns) - 30)]
    cp_idx = np.argmax(scores) + 30
    cp_date = df["Date"].iloc[cp_idx]

    plt.figure(figsize=(14, 5))
    plt.plot(df["Date"], log_returns, label="Log Returns", alpha=0.6)
    plt.axvline(cp_date, color="red", linestyle="--", label=f"Changepoint: {cp_date.date()}")
    plt.title("Clean Changepoint Detection in Brent Oil Log Returns")
    plt.xlabel("Date")
    plt.ylabel("Log Return")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    os.makedirs("reports/figures", exist_ok=True)
    plt.savefig("reports/figures/changepoint_clean_block.png")
    plt.close()

if __name__ == "__main__":
    run_changepoint_detector()
