-- 2_1.sql
-- Найти и вывести всю информацию о каждом заказе:
-- имя покупателя, имя продавца (менеджера), сумму, дату.

SELECT
    c.full_name      AS customer_name,
    m.full_name      AS manager_name,
    o.purchase_amount,
    o.date
FROM "order" AS o
LEFT JOIN customer AS c
    ON o.customer_id = c.customer_id
LEFT JOIN manager  AS m
    ON o.manager_id = m.manager_id;