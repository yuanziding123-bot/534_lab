# 534_lab — Treasury market dashboard

A static web page (`index.html`) served by GitHub Pages that fetches and displays U.S. Treasury market data:

- **Overview** – latest yields, 1-month changes, yield curve and a change table
- **Yields** – history for any maturity
- **Spreads** – 10y–2y / 10y–3m term spreads and corporate credit spreads
- **Inflation** – CPI, breakeven inflation and the real 10-year yield
- **Scenarios** – reprices par bonds under parallel, steepener and flattener shocks
- **Monte Carlo** – thousands of simulated yield paths (random walk or Vasicek mean reversion)

## How it works

1. `scripts/fetch_data.py` downloads the series from [FRED](https://fred.stlouisfed.org/) into `data.json`
   (FRED blocks direct browser requests, so the data is fetched ahead of time).
2. `index.html` fetches `data.json` and draws everything in the browser with Chart.js.
3. A GitHub Action (`.github/workflows/update-data.yml`) refreshes `data.json` every weekday.
4. GitHub Pages serves the site from the `main` branch root.

Run locally: `python -m http.server` then open http://localhost:8000.
