with orders as (
    select * from {{ ref('stg_orders') }}
    where order_status = 'completed'
),

products as (
    select * from {{ ref('stg_products') }}
),

joined as (
    select
        o.order_day,
        o.quantity * p.price as line_revenue
    from orders o
    inner join products p on o.product_id = p.product_id
)

select
    order_day,
    round(sum(line_revenue), 2) as total_revenue,
    count(*)                    as total_line_items
from joined
group by order_day
order by order_day
