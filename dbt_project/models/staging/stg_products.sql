with source as (
    select * from {{ source('raw', 'raw_products') }}
)

select
    product_id,
    product_name,
    category,
    cast(price as decimal(10, 2)) as price
from source
