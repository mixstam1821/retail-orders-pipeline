with orders as (
    select * from {{ ref('stg_orders') }}
    where order_status = 'completed'
),

products as (
    select * from {{ ref('stg_products') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

order_value as (
    select
        o.customer_id,
        o.order_id,
        o.order_day,
        o.quantity * p.price as line_revenue
    from orders o
    inner join products p on o.product_id = p.product_id
)

select
    c.customer_id,
    c.customer_name,
    c.country,
    count(distinct ov.order_id)     as total_orders,
    round(sum(ov.line_revenue), 2)  as lifetime_value,
    min(ov.order_day)               as first_order_date,
    max(ov.order_day)               as last_order_date
from customers c
left join order_value ov on c.customer_id = ov.customer_id
group by c.customer_id, c.customer_name, c.country
order by lifetime_value desc
