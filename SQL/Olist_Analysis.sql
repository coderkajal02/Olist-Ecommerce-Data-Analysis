use olist_analytics;
SELECT COUNT(*) AS total_rows
FROM orders_import_python;

USE olist_analytics;

SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT order_id) AS unique_orders
FROM orders_import_python;
ORDER BY total_orders DESC;

SELECT *
FROM orders_import_fixed
LIMIT 10;

SELECT
    COUNT(*) AS total_orders,
    SUM(order_approved_at IS NULL) AS missing_approval,
    SUM(order_delivered_carrier_date IS NULL) AS missing_carrier_date,
    SUM(order_delivered_customer_date IS NULL) AS missing_delivery_date,
    SUM(delivery_days IS NULL) AS missing_delivery_days
FROM orders_import_python;


-- --Query 1: Order status analysis
-- Business question: How many orders are delivered, canceled, shipped, or in other statuses?

select order_status,
count(*) as total_orders
from orders_import_python
group by order_status
order by total_orders Desc;

-- Step 2 – Monthly order trend
-- Business question: How many orders did the company receive each month?
select date_format(order_purchase_timestamp, '%y-%m') as order_month,
count(*) as total_orders
from orders_import_python
group by date_format(order_purchase_timestamp, '%y-%m')
order by order_month;

-- Step 3 – Average delivery time 
-- Business question: On average, how many days does an order take to reach the customer?
select round(avg(delivery_days),2) as avg_delivery_days
from orders_import_python
where delivery_days IS NOT NULL;

-- Step 4 – Delivery performance analysis
-- Business question: How many orders were delivered on time, delayed, or not delivered?
select delivery_status,
count(*)as total_orders
from orders_import_python
group by delivery_status
order by total_orders;

-- Step 5 – Calculate delayed delivery percentage using SQL
select 
round(
sum(case when delivery_status = 'Delayed'
then 1 else 0 end) * 100.0/count(*),2) as delayed_percentage
from orders_import_python;

-- Step 6 – Find the top 10 oldest orders
-- Business question: Which orders were placed earliest?

select order_id, 
order_status,
order_purchase_timestamp
from orders_import_python
order by order_purchase_timestamp asc
limit 10;

select database();
show tables;


SELECT
    (SELECT COUNT(*) FROM order_items_import_python) AS total_items,
    (SELECT COUNT(*) FROM order_payments_import_python) AS total_payments;
