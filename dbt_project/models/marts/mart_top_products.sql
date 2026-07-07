with orders as (
    select * from {{ ref('stg_orders') }}
    where order_status = 'completed'
),

products as (
    select * from {{ ref('stg_products') }}
),

joined as (
    select
        p.product_id,
        p.product_name,
        p.category,
        o.quantity,
        o.quantity * p.price as line_revenue
    from orders o
    inner join products p on o.product_id = p.product_id
)

select
    product_id,
    product_name,
    category,
    sum(quantity)               as total_quantity_sold,
    round(sum(line_revenue), 2) as total_revenue,
    rank() over (order by sum(line_revenue) desc) as revenue_rank
from joined
group by product_id, product_name, category
order by total_revenue desc
