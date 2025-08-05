from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

DATA_PATH = "data/processed/cleaned_data.csv"
EVENT_PATH = "data/raw/events.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

def load_events():
    events = pd.read_csv(EVENT_PATH)
    events["Date"] = pd.to_datetime(events["Date"], errors="coerce")
    return events

@app.route("/api/data")
def get_oil_prices():
    df = load_data()
    df = df.rename(columns={"Date": "date", "Price": "price"})
    return jsonify(df[["date", "price"]].to_dict(orient="records"))  # Removed .tail(60)

@app.route("/api/summary")
def get_summary():
    df = load_data()
    price_diff = df["Price"].diff().dropna()
    return {
        "volatility": round(float(price_diff.std()), 4),
        "avg_daily_change": round(float(price_diff.mean()), 4)
    }

@app.route("/api/forecast")
def forecast():
    df = load_data()
    df["Forecast"] = df["Price"].rolling(3).mean().fillna(method="bfill")
    df = df.rename(columns={"Date": "date", "Price": "price", "Forecast": "forecast"})
    return jsonify(df[["date", "price", "forecast"]].to_dict(orient="records"))  # All rows

@app.route("/api/events")
def get_events():
    df = load_data()
    events = load_events()

    result = []
    for _, event in events.iterrows():
        date = event["Date"]
        if pd.isna(date):
            continue

        idx = df["Date"].searchsorted(date)
        before = df.iloc[max(0, idx - 3):idx]
        after = df.iloc[idx:min(len(df), idx + 3)]

        delta = after["Price"].mean() - before["Price"].mean()
        impact = None if pd.isna(delta) else round(delta, 2)

        result.append({
            "date": date.strftime("%Y-%m-%d"),
            "event": event.get("Event", ""),
            "type": event.get("Type", ""),
            "source": event.get("Source", ""),
            "expected_impact": event.get("Expected Impact (%)", ""),
            "actual_impact": impact
        })

    return jsonify(result)

@app.route("/api/metrics")
def metrics():
    return jsonify({
        "rmse": [
            {"model": "ARIMA", "value": 1.12},
            {"model": "Bayesian", "value": 0.98}
        ]
    })

@app.route("/api/macros")
def macros():
    return jsonify({
        "GDP_growth": 2.5,
        "inflation_rate": 5.7,
        "exchange_rate": 0.83
    })

@app.route("/api/sentiment")
def sentiment():
    return jsonify({
        "positive": 62,
        "neutral": 28,
        "negative": 10
    })

if __name__ == "__main__":
    app.run(debug=True)
