"use client";

import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale, LinearScale,
  PointElement, LineElement,
  Tooltip, Legend
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

const endpoints = [
  "data", "forecast", "events", "summary",
  "sentiment", "macros", "metrics"
];

type APIResponse = Record<string, any>;
type Errors = Record<string, string>;

export default function Dashboard() {
  const [apiData, setApiData] = useState<APIResponse>({});
  const [errorLog, setErrorLog] = useState<Errors>({});
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [eventType, setEventType] = useState("All");
  const [region, setRegion] = useState("All");

  useEffect(() => {
    const fetchData = async () => {
      const dataStore: APIResponse = {};
      const errorStore: Errors = {};

      for (const endpoint of endpoints) {
        try {
          const res = await fetch(`http://127.0.0.1:5000/api/${endpoint}`);
          if (!res.ok) throw new Error(`Status ${res.status}`);
          dataStore[endpoint] = await res.json();
        } catch (err: unknown) {
          const msg = err instanceof Error ? err.message : "Fetch failed";
          errorStore[endpoint] = msg;
          console.error(`Fetch error [${endpoint}]:`, msg);
        }
      }

      setApiData(dataStore);
      setErrorLog(errorStore);
    };

    fetchData();
  }, []);

  const filterByDateRange = (data: any[]) => {
    if (!startDate && !endDate) return data;
    return data.filter((d: any) => {
      const date = new Date(d.date);
      const afterStart = startDate ? date >= new Date(startDate) : true;
      const beforeEnd = endDate ? date <= new Date(endDate) : true;
      return afterStart && beforeEnd;
    });
  };

  const filterEvents = (events: any[]) => {
    return events.filter((e: any) => {
      const typeMatch = eventType === "All" || e.type === eventType;
      const regionMatch = region === "All" || e.source === region || e.region === region;
      return typeMatch && regionMatch;
    });
  };

  const getDropdownOptions = (key: string) => {
    const values = Array.from(new Set(apiData.events?.map((e: any) => e[key])));
    return ["All", ...values];
  };

  return (
    <main style={{ padding: "2rem", maxWidth: "960px", margin: "auto", fontFamily: "Segoe UI, sans-serif" }}>
      <h1 style={{ textAlign: "center", color: "#1e3a8a" }}>🌍 Brent Oil Analysis Dashboard</h1>

      {/* 📅 Time Range Filter */}
      <section style={{ marginBottom: "2rem" }}>
        <h3>📅 Filter by Date</h3>
        <div style={{ display: "flex", gap: "1rem" }}>
          <label>Start: <input type="date" value={startDate} onChange={e => setStartDate(e.target.value)} /></label>
          <label>End: <input type="date" value={endDate} onChange={e => setEndDate(e.target.value)} /></label>
        </div>
      </section>

      {/* 🛑 Error Logging */}
      {Object.keys(errorLog).length > 0 && (
        <section>
          <h2 style={{ color: "darkred" }}>⚠️ Errors</h2>
          <ul>
            {Object.entries(errorLog).map(([key, err], i) => (
              <li key={i}><strong>{key}</strong>: {err}</li>
            ))}
          </ul>
        </section>
      )}

      {/* 🛢️ Brent Price Chart */}
      {apiData.data && !errorLog.data && (
        <section>
          <h2>🛢️ Brent Price</h2>
          <Line data={{
            labels: filterByDateRange(apiData.data).map((d: any) => d.date),
            datasets: [{
              label: "Price",
              data: filterByDateRange(apiData.data).map((d: any) => d.price),
              borderColor: "#007aff"
            }]
          }} />
        </section>
      )}

      {/* 🔮 Forecast Chart */}
      {apiData.forecast && !errorLog.forecast && (
        <section>
          <h2>🔮 Forecast vs Actual</h2>
          <Line data={{
            labels: filterByDateRange(apiData.forecast).map((d: any) => d.date),
            datasets: [
              {
                label: "Actual",
                data: filterByDateRange(apiData.forecast).map((d: any) => d.price),
                borderColor: "#007aff"
              },
              {
                label: "Forecast",
                data: filterByDateRange(apiData.forecast).map((d: any) => d.forecast),
                borderColor: "#ff9800",
                borderDash: [5, 5]
              }
            ]
          }} />
        </section>
      )}

      {/* 🌍 Event Filters and Listing */}
      {apiData.events && !errorLog.events && (
        <section>
          <h2>🌍 Event Impact on Prices</h2>
          <div style={{ display: "flex", gap: "1rem", marginBottom: "1rem" }}>
            <label>
              Type:
              <select value={eventType} onChange={e => setEventType(e.target.value)}>
                {getDropdownOptions("type").map((t, i) => (
                  <option key={i} value={String(t)}>{String(t)}</option>
                ))}
              </select>
            </label>
            <label>
              Source:
              <select value={region} onChange={e => setRegion(e.target.value)}>
                {getDropdownOptions("source").map((r, i) => (
                  <option key={i} value={String(r)}>{String(r)}</option>
                ))}
              </select>
            </label>
          </div>
          <ul style={{ paddingLeft: 0 }}>
            {filterEvents(apiData.events).map((e: any, i) => (
              <li key={i} style={{
                listStyle: "none", marginBottom: "1rem",
                background: "#fff", padding: "1rem",
                borderRadius: "8px", boxShadow: "0 2px 4px rgba(0,0,0,0.1)"
              }}>
                <strong>{e.event}</strong> ({e.date})<br />
                Type: {e.type} | Δ Price: <strong>{e.actual_impact}</strong><br />
                Source of information: {e.source}
              </li>
            ))}
          </ul>
        </section>
      )}

      {/* 📈 Summary Section */}
      {apiData.summary && !errorLog.summary && (
        <section>
          <h2>📈 Summary</h2>
          <p>Volatility: <strong>{apiData.summary.volatility}</strong></p>
          <p>Avg Daily Change: <strong>{apiData.summary.avg_daily_change}</strong></p>
        </section>
      )}

      {/* 📊 Metrics */}
      {apiData.metrics && !errorLog.metrics && (
        <section>
          <h2>📊 Model Metrics</h2>
          <ul>
            {apiData.metrics.rmse.map((m: any, i: number) => (
              <li key={i}>{m.model}: RMSE = {m.value}</li>
            ))}
          </ul>
        </section>
      )}

      {/* 💹 Macros */}
      {apiData.macros && !errorLog.macros && (
        <section>
          <h2>💹 Macro Indicators</h2>
          <p>GDP Growth: <strong>{apiData.macros.GDP_growth}%</strong></p>
          <p>Inflation Rate: <strong>{apiData.macros.inflation_rate}%</strong></p>
          <p>Exchange Rate: <strong>{apiData.macros.exchange_rate}</strong></p>
        </section>
      )}

      {/* 💬 Sentiment */}
      {apiData.sentiment && !errorLog.sentiment && (
        <section>
          <h2>💬 Sentiment Analysis</h2>
          <p>Positive: {apiData.sentiment.positive}</p>
          <p>Neutral: {apiData.sentiment.neutral}</p>
          <p>Negative: {apiData.sentiment.negative}</p>
        </section>
      )}
    </main>
  );
}
