{{
    config(
        materialized='view'
    )
}}

with zones as (
    select * from {{ ref("zones") }}
    where 'borough' != 'Unknown'
),
taxi_trips as (
    select * from {{ ref("stg_silver_layer__yellow_taxi_trips") }}
)
select
    taxi_trips.pickup_locationid,
    zones.zone as pickup_zone,
    {{ dbt.date_trunc("month", "pickup_datetime") }} as revenue_month, 
    sum(total_amount) as revenue_monthly_total_amount
from zones inner join taxi_trips 
on  zones.locationid = taxi_trips.pickup_locationid
group by taxi_trips.pickup_locationid, pickup_zone, revenue_month