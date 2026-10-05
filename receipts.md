# Receipts — $0 warehouse (2026-08)

Measured from the actual run. Reproduce: `python load.py && python run_all.py`.

| Receipt | Value |
| --- | --- |
| Month loaded | 2026-08 |
| Raw rows loaded | 3336716 |
| Rows after staging filters | 3278983 |
| Rows filtered out | 57733 |
| dbt build results passing | 10 |
| Days in daily fact table | 31 |
| Transform + test runtime (dbt build) | 6.1 s |
| Monthly infrastructure cost | $0 |

Month summary (from `mart_month_summary`):

| month | trips | revenue | avg_distance_miles | tip_pct_of_fare |
| --- | --- | --- | --- | --- |
| 2026-08 | 3278983 | 99652254.68 | 3.59 | 12.8 |

Exports: [fct_daily_trips.csv](exports/fct_daily_trips.csv) · [mart_month_summary.csv](exports/mart_month_summary.csv)
