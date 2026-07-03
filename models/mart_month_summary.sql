select
  (select month from {{ source('raw', 'load_meta') }}) as month,
  count(*) as trips,
  round(sum(total_amount), 2) as revenue,
  round(avg(trip_distance), 2) as avg_distance_miles,
  round(sum(tip_amount) / nullif(sum(fare_amount), 0) * 100, 1) as tip_pct_of_fare
from {{ ref('stg_trips') }}
