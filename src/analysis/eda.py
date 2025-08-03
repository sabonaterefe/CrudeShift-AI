import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
import os

# ──📁 Path Configurations ──────────────────
RAW_DATA_PATH = "data/raw/BrentOilPrices.csv"
PROCESSED_DATA_DIR = "data/processed/"
PROCESSED_DATA_PATH = os.path.join(PROCESSED_DATA_DIR, "cleaned_data.csv")
PLOTS_DIR = "reports/figures/"

# Ensure necessary folders exist
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

# ──⚙️ Preprocessing ────────────────────────
def preprocess_brent_data(input_path=RAW_DATA_PATH, output_path=PROCESSED_DATA_PATH):
    """
    Loads and processes Brent oil price data with mixed date formats.
    - Infers dates robustly
    - Sorts chronologically
    - Computes log returns
    - Saves cleaned file to 'data/processed/cleaned_data.csv'
    """
    df = pd.read_csv(input_path)

    # Parse date column using mixed inference
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["Date"])  # Drop rows where date parsing failed

    df = df.sort_values("Date").reset_index(drop=True)

    # Calculate log returns
    df["LogReturn"] = np.log(df["Price"]).diff()
    df.dropna(inplace=True)

    df.to_csv(output_path, index=False)
    return df

# ──📊 Exploratory Analysis ─────────────────
def run_eda(df):
    """
    Generates key EDA plots and stationarity test.
    Saves plots to 'reports/figures/'.
    """
    # Plot time series
    plt.figure(figsize=(14, 5))
    sns.lineplot(x="Date", y="Price", data=df, color="navy")
    plt.title("Brent Oil Prices Over Time")
    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "price_timeseries.png"))
    plt.close()

    # Plot log return distribution
    plt.figure(figsize=(10, 5))
    sns.histplot(df["LogReturn"], bins=100, kde=True, color="steelblue")
    plt.title("Distribution of Daily Log Returns")
    plt.xlabel("Log Return")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(PLOTS_DIR, "logreturn_distribution.png"))
    plt.close()

    # Stationarity check
    result = adfuller(df["LogReturn"])
    print(f"ADF Statistic: {result[0]:.4f}")
    print(f"p-value: {result[1]:.4f}")
    if result[1] < 0.05:
        print("✅ Log returns are stationary — good for time-series modeling.")
    else:
        print("⚠️ Non-stationary — consider differencing or transformation.")

# ──🚀 Script Entry Point ──────────────────
if __name__ == "__main__":
    df = preprocess_brent_data()
    run_eda(df)
