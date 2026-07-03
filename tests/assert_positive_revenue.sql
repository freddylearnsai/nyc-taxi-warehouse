select * from {{ ref('fct_daily_trips') }} where revenue < 0 or trips <= 0
