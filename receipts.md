# Receipts — $0 warehouse (2026-05)

Measured from the actual run. Reproduce: `python load.py && python run_all.py`.

| Receipt | Value |
| --- | --- |
| Month loaded | 2026-05 |
| Raw rows loaded | 4090836 |
| Rows after staging filters | 4023818 |
| Rows filtered out | 67018 |
| dbt build results passing | 10 |
| Days in daily fact table | 31 |
| Transform + test runtime (dbt build) | 2.7 s |
| Monthly infrastructure cost | $0 |

Month summary (from `mart_month_summary`):

| month | trips | revenue | avg_distance_miles | tip_pct_of_fare |
| --- | --- | --- | --- | --- |
| 2026-05 | 4023818 | 123678720.68 | 3.43 | 13.7 |

Exports: [fct_daily_trips.csv](exports/fct_daily_trips.csv) · [mart_month_summary.csv](exports/mart_month_summary.csv)
