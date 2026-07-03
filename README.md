# nyc-taxi-warehouse

A $0/month data warehouse that runs itself: NYC TLC yellow-taxi data, loaded into DuckDB, modeled and tested with dbt, scheduled on GitHub Actions — built in public by [freddyxai](https://freddyxai.com/work-with-me).

Status: build in progress. Receipts land in `receipts.md` when the first run completes.

## Reproduce

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python load.py       # newest available TLC month → warehouse.duckdb (raw schema)
.venv/bin/python run_all.py    # dbt build + tests → exports/ + receipts.md
```
