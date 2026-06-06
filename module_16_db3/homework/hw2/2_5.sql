-- 2_5.sql
-- Вернуть уникальные пары покупателей, живущих в одном городе
-- и имеющих одного менеджера.

SELECT
    c1.full_name AS customer1_name,
    c2.full_name AS customer2_name,
    c1.city      AS city,
    m.full_name  AS manager_name
FROM customer AS c1
JOIN customer AS c2
    ON c1.customer_id < c2.customer_id
   AND c1.city = c2.city
   AND c1.manager_id = c2.manager_id
JOIN manager AS m
    ON c1.manager_id = m.manager_id
