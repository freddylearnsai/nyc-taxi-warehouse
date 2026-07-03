"""Timed pipeline: dbt build -> counts -> exports -> receipts.md. Assumes load.py already ran."""
import json, re, subprocess, time
import duckdb

t0 = time.time()
build = subprocess.run([".venv/bin/dbt", "build", "--profiles-dir", "."],
                       capture_output=True, text=True)
print(build.stdout[-2000:])
if build.returncode != 0:
    raise SystemExit("dbt build failed — receipts not written")
m = re.search(r"Done\. PASS=(\d+) WARN=(\d+) ERROR=(\d+) SKIP=(\d+)", build.stdout)
passed = m.group(1) if m else "unknown"

con = duckdb.connect("warehouse.duckdb")
month = con.execute("select month from raw.load_meta").fetchone()[0]
raw_rows = con.execute("select count(*) from raw.yellow_trips").fetchone()[0]
stg_rows = con.execute("select count(*) from stg_trips").fetchone()[0]
daily = con.execute("select count(*) from fct_daily_trips").fetchone()[0]

# Adapt-point: summary.to_markdown() needs pandas (via fetchdf()) + tabulate, and neither
# is installed in .venv (dbt-duckdb does not pull pandas in transitively here — confirmed
# by `import pandas` failing). Rather than add two new deps, pull the one summary row as a
# plain tuple via fetchone() and format the markdown table by hand. Zero new dependencies.
summary_cols = [d[0] for d in con.execute("select * from mart_month_summary").description]
summary_row = con.execute("select * from mart_month_summary").fetchone()
summary_header = "| " + " | ".join(summary_cols) + " |"
summary_sep = "| " + " | ".join(["---"] * len(summary_cols)) + " |"
summary_values = "| " + " | ".join(str(v) for v in summary_row) + " |"
summary_table = "\n".join([summary_header, summary_sep, summary_values])

con.execute("copy fct_daily_trips to 'exports/fct_daily_trips.csv' (header, delimiter ',')")
con.execute("copy mart_month_summary to 'exports/mart_month_summary.csv' (header, delimiter ',')")
secs = round(time.time() - t0, 1)

receipts = f"""# Receipts — $0 warehouse ({month})

Measured from the actual run. Reproduce: `python load.py && python run_all.py`.

| Receipt | Value |
| --- | --- |
| Month loaded | {month} |
| Raw rows loaded | {raw_rows} |
| Rows after staging filters | {stg_rows} |
| Rows filtered out | {raw_rows - stg_rows} |
| dbt build results passing | {passed} |
| Days in daily fact table | {daily} |
| Transform + test runtime (dbt build) | {secs} s |
| Monthly infrastructure cost | $0 |

Month summary (from `mart_month_summary`):

{summary_table}

Exports: [fct_daily_trips.csv](exports/fct_daily_trips.csv) · [mart_month_summary.csv](exports/mart_month_summary.csv)
"""
open("receipts.md", "w").write(receipts)
print(json.dumps({"month": month, "raw_rows": raw_rows, "stg_rows": stg_rows,
                  "dbt_passing": passed, "days": daily, "dbt_seconds": secs}))
