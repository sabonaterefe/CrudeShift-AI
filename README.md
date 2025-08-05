# Brent Oil Log Return Analysis & Changepoint Detection

This project analyzes historical Brent crude oil prices and identifies regime shifts using both statistical and Bayesian methods. It is split into two primary tasks:

---

## Task 1 — Data Cleaning & Exploratory Analysis

The goal of Task 1 is to build a reliable preprocessing pipeline and perform detailed exploratory data analysis (EDA).

### Completed Work

## Raw Price Import  
  Loaded `BrentOilPrices.csv` from `data/raw/` into `pandas`, with robust column checks and error handling.

  ## Date Parsing & Cleaning  
  Implemented a flexible multi-format date parser supporting `%d-%b-%y`, `%Y-%m-%d`, `%d/%m/%Y`, and `%Y/%m/%d` formats with fallback coercion.

  ## Preprocessing Module 
  Created `preprocess_brent_data()` in `src/analysis/eda.py` to handle:
  - Raw date string cleanup via regex
  - Conversion to datetime objects
  - Calculation of daily log returns
  - Filtering and NaN handling

  ## Exported Clean Data  
  Final cleaned dataset saved to:  
  `data/processed/cleaned_data.csv`

  ## Exploratory Visualizations
  - Time series of Brent prices: `reports/figures/price_timeseries.png`
  - Log return distribution: `reports/figures/logreturn_distribution.png`

  ## Stationarity Testing
  - Applied Augmented Dickey–Fuller test (ADF) on log returns
  - Printed summary and verdict (stationary if p < 0.05)

  ## Event Annotation
  Marked major oil market events on price timeline:
  - `2008-09-15`: Lehman Collapse  
  - `2014-11-27`: OPEC Keeps Output  
  - `2020-03-06`: OPEC+ Breakdown

---

## Task 2 — Modeling Regime Shifts (Changepoints)

This task explores multiple approaches to changepoint detection in oil price log returns.

### ✔Completed Work

## Fast Likelihood-Based Estimator
  Implemented `split_likelihood()` inside `change_point_model.py`  
  - Offline, non-Bayesian method  
  - Computes split point via negative log-likelihood comparison  
  - Executes in under 1 second

  ## Bayesian Changepoint Detection (PyMC)
  - Modeled log returns with discrete changepoint `τ`
  - Two regimes with separate means (`μ1`, `μ2`)
  - Shared standard deviation (`σ`)
  - Sampled posterior using PyMC’s NUTS
  - Extracted posterior distribution and summary stats

 ## Posterior Visualization
  - Posterior trace plots via `arviz`
  - Histogram of changepoint samples (`τ`) with interpretation

 ## Figure Output
  Saved annotated changepoint plot to:  
  `reports/figures/changepoint_clean_block.png`
  

##  Dependencies

Install required packages with:

pip install -r requirements.txt

Dependencies include:

pandas, numpy, matplotlib, seaborn

pymc, arviz

statsmodels

Branches Overview
Branch Name	Purpose
data-prep	All preprocessing, cleaning, and EDA
modeling	Both fast and Bayesian changepoint models, figures

## Frontend Enhancements
Built with Next.js App Router + TypeScript, the dashboard lives in frontend/src/app/page.tsx.

Integrated Chart.js with zoom/pan support via chartjs-plugin-zoom.

Implemented downsampling for large datasets using client-side rolling averages for smoother rendering.

Date Range Filtering:

Users can narrow time series views using startDate and endDate inputs.

Applies to both raw price and forecasted views.

Event Filtering:

Sidebar filters for event type and region (from event source).

Event list only appears when a valid filter is selected.

Robust error handling and fallback logic prevents UI crashes due to missing or malformed API data.

## API Endpoints
Route	Description
/api/data	Full Brent price history
/api/forecast	Rolling average forecast estimates
/api/events	Annotated market events with impact
/api/summary	Volatility and daily change stats
/api/sentiment	Static market sentiment indicators
/api/macros	GDP growth, inflation, currency rate
/api/metrics	Model RMSE for changepoint algorithms
All served via Flask with CORS enabled.

## Running Locally
Backend (Flask)
cd backend
python app.py
Frontend (Next.js)

cd frontend
npm install
npm run dev
Ensure both servers are running on:

Flask: http://127.0.0.1:5000

Next: http://localhost:3000

## Testing & Validation
Manual checks across endpoints for correctness and response shape

Type-safe filtering of frontend data against undefined/NaN entries

Verified JSON compatibility across null, strings, floats

Performed changepoint model validation via posterior trace review

Chart interactivity tested with large datasets (8000+ records)

## Completed Tasks Overview
Task	Summary	Status
Task 1	Data cleanup, log return calc, EDA	, Done
Task 2	Fast and Bayesian changepoint modeling	, Done
Task 3	Dashboard with filters, charts, API backend	, Done

