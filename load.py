"""Load the newest available TLC yellow-taxi month into warehouse.duckdb (schema raw)."""
import datetime as dt, json, time, urllib.request
import duckdb

BASE = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month}.parquet"

def candidate_months(n: int = 6) -> list[str]:
    d = dt.date.today().replace(day=1)
    out = []
    for _ in range(n):
        d = (d - dt.timedelta(days=1)).replace(day=1)
        out.append(d.strftime("%Y-%m"))
    return out  # newest first, starting last month

def newest_available() -> str:
    for m in candidate_months():
        req = urllib.request.Request(BASE.format(month=m), method="HEAD")
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                if r.status == 200:
                    return m
        except Exception:
            continue
    raise SystemExit("no TLC month found in the last 6 — aborting, do not fabricate")

def main() -> None:
    t0 = time.time()
    month = newest_available()
    url = BASE.format(month=month)
    path = "data/yellow.parquet"
    urllib.request.urlretrieve(url, path)
    con = duckdb.connect("warehouse.duckdb")
    con.execute("create schema if not exists raw")
    con.execute("create or replace table raw.yellow_trips as select * from read_parquet('data/yellow.parquet')")
    rows = con.execute("select count(*) from raw.yellow_trips").fetchone()[0]
    con.execute("""create or replace table raw.load_meta as
                   select ? as month, ? as source_url, current_timestamp as loaded_at""", [month, url])
    print(json.dumps({"month": month, "rows": rows, "load_seconds": round(time.time() - t0, 1)}))

if __name__ == "__main__":
    main()
