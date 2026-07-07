with source as (
    select * from {{ source('raw', 'raw_orders') }}
)

select
    order_id,
    customer_id,
    product_id,
    cast(order_date as timestamp) as order_date,
    cast(order_date as date)      as order_day,
    quantity,
    order_status
from source
