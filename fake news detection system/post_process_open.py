# filepath: c:\Users\user\Desktop\fake news detection system\fake news detection system\post_process_open.py
import pandas as pd
import os
import sys

OUT_CSV = os.path.join("data", "kaggle_news_dataset.csv")
REPORT = "report.html"

if not os.path.exists(OUT_CSV):
    print(f"[ERROR] Output CSV not found: {OUT_CSV}")
    sys.exit(1)

df = pd.read_csv(OUT_CSV)

# Limit rows for quicker load in browser (adjust as needed)
preview_rows = 500
html_table = df.head(preview_rows).to_html(index=False, classes="table", border=0, escape=False)

html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>Kaggle News Dataset (preview)</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial; margin: 20px; }}
    table {{ border-collapse: collapse; width: 98%; margin: 10px auto; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; }}
    th {{ background: #f4f4f4; }}
    h1 {{ text-align:center; }}
  </style>
</head>
<body>
  <h1>Kaggle News Dataset (preview: {min(preview_rows, len(df))} rows)</h1>
  {html_table}
  <p style="text-align:center;">Full CSV: {OUT_CSV}</p>
</body>
</html>"""

with open(REPORT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"[OK] Report written: {REPORT}")
