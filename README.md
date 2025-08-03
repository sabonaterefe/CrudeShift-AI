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
  - 📈 Time series of Brent prices: `reports/figures/price_timeseries.png`
  - 📊 Log return distribution: `reports/figures/logreturn_distribution.png`

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
# Next Steps
Generalize modeling for multiple changepoints (e.g. ruptures)

Add markdown reporting in reports/

Enable CLI-based execution with parameterized controls

Improve changepoint interpretability using macroeconomic overlays

Built and maintained by Sabona with modularity, precision, and statistical elegance.
