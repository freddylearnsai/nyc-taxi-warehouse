# nyc-taxi-warehouse

A $0/month data warehouse that runs itself: NYC TLC yellow-taxi data, loaded into DuckDB, modeled and tested with dbt, scheduled on GitHub Actions — built in public by [freddyxai](https://freddyxai.com/work-with-me).

**Receipts:** see [receipts.md](receipts.md) — every number measured from a real run. The warehouse re-runs itself on the 5th of every month via GitHub Actions — see [the workflow](.github/workflows/warehouse.yml) and [run history](https://github.com/freddylearnsai/nyc-taxi-warehouse/actions).

Built by [freddyxai](https://freddyxai.com) — your data team, on demand. This is the shape of a [$1,000–$2,000 automation build](https://freddyxai.com/work-with-me): a warehouse that runs itself for $0/month.

## Reproduce

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python load.py       # newest available TLC month → warehouse.duckdb (raw schema)
.venv/bin/python run_all.py    # dbt build + tests → exports/ + receipts.md
```
