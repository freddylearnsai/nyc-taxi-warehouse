with month_window as (
  select
    strptime(month || '-01', '%Y-%m-%d')::timestamp as month_start,
    (strptime(month || '-01', '%Y-%m-%d')::timestamp + interval 1 month) as month_end
  from {{ source('raw', 'load_meta') }}
)
select
  t.tpep_pickup_datetime  as picked_up_at,
  t.tpep_dropoff_datetime as dropped_off_at,
  t.passenger_count, t.trip_distance, t.payment_type,
  t.fare_amount, t.tip_amount, t.total_amount
from {{ source('raw', 'yellow_trips') }} t, month_window w
where t.tpep_dropoff_datetime > t.tpep_pickup_datetime
  and t.tpep_pickup_datetime >= w.month_start and t.tpep_pickup_datetime < w.month_end
  and t.trip_distance >= 0 and t.trip_distance < 500
  and t.total_amount >= 0 and t.total_amount < 10000
