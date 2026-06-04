-- 2_2.sql
-- Найти имена покупателей, которые не сделали ни одного заказа.

SELECT
    c.full_name
FROM customer AS c
LEFT JOIN "order" AS o
    ON o.customer_id = c.customer_id
WHERE o.order_no IS NULL
