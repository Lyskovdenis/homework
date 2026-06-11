-- 6. Средняя оценка за задания «прочитать и выучить»
SELECT AVG(ag.grade) AS avg_grade_read_learn
FROM assignments_grades ag
JOIN assignments a ON ag.assisgnment_id = a.assisgnment_id
WHERE LOWER(a.assignment_text) LIKE '%прочитать%'
   OR LOWER(a.assignment_text) LIKE '%выучить%';