-- 2_4.sql
-- Для покупателей, которые сделали заказ напрямую (без помощи менеджеров),
-- вывести имена и номера заказов.

SELECT
    c.full_name AS customer_name,
    o.order_no
FROM "order" AS o
JOIN customer AS c
    ON o.customer_id = c.customer_id
WHERE o.manager_id IS NULL
