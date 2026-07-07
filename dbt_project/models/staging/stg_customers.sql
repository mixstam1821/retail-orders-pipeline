with source as (
    select * from {{ source('raw', 'raw_customers') }}
)

select
    customer_id,
    name        as customer_name,
    email,
    country,
    cast(signup_date as date) as signup_date
from source
