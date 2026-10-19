"""Download Treasury yields, spreads and inflation from FRED into data.json.

FRED's CSV endpoint needs no API key but does not allow browser (CORS) requests,
so this script runs ahead of time (locally or in GitHub Actions) and the page
fetches the resulting data.json from the same site.
"""
import csv
import io
import json
import time
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

START = "2000-01-01"
SERIES = {
    # Treasury constant-maturity yields (daily, %)
    "DGS3MO": "3 mo", "DGS6MO": "6 mo", "DGS1": "1 yr", "DGS2": "2 yr",
    "DGS5": "5 yr", "DGS7": "7 yr", "DGS10": "10 yr", "DGS20": "20 yr", "DGS30": "30 yr",
    # Spreads and market inflation expectations (daily)
    "T10Y2Y": "10 yr minus 2 yr", "T10Y3M": "10 yr minus 3 mo",
    "T10YIE": "10 yr breakeven inflation", "T5YIE": "5 yr breakeven inflation",
    "BAMLC0A0CM": "Investment-grade corporate OAS", "BAMLH0A0HYM2": "High-yield corporate OAS",
    # Inflation (monthly index)
    "CPIAUCSL": "CPI, all items", "CPILFESL": "CPI, core",
}


def fetch(series_id):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={START}"
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8.0", "Accept": "*/*"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                text = r.read().decode()
            break
        except Exception:
            if attempt == 3:
                raise
            time.sleep(3 * (attempt + 1))
    rows = list(csv.reader(io.StringIO(text)))[1:]
    out = []
    for d, v in rows:
        if v not in ("", "."):
            out.append([d, round(float(v), 3)])
    return out


def main():
    data = {}
    for sid, label in SERIES.items():
        obs = fetch(sid)
        print(f"{sid:14s} {len(obs):6d} obs, last {obs[-1]}")
        data[sid] = {"label": label, "dates": [o[0] for o in obs], "values": [o[1] for o in obs]}
    payload = {
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "asOf": data["DGS10"]["dates"][-1],
        "series": data,
    }
    out = Path(__file__).resolve().parent.parent / "data.json"
    out.write_text(json.dumps(payload, separators=(",", ":")))
    print(f"wrote {out} ({out.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
