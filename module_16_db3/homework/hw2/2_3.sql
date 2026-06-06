-- 2_3.sql
-- Вывести номер заказа, имена продавца и покупателя,
-- если место жительства продавца и покупателя не совпадает.

SELECT
    o.order_no,
    m.full_name AS manager_name,
    c.full_name AS customer_name
FROM "order" AS o
JOIN customer AS c
    ON o.customer_id = c.customer_id
JOIN manager  AS m
    ON o.manager_id = m.manager_id
WHERE c.city <> m.city
