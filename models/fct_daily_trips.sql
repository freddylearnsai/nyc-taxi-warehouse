select
  cast(date_trunc('day', picked_up_at) as date) as trip_date,
  count(*) as trips,
  round(sum(total_amount), 2) as revenue,
  round(avg(trip_distance), 2) as avg_distance_miles,
  round(avg(total_amount), 2) as avg_total
from {{ ref('stg_trips') }}
group by 1
order by 1
