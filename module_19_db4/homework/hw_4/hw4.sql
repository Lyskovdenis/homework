-- Среднее, максимум и минимум просроченных заданий для каждого класса (группы)
SELECT ssg.group_id,
       AVG(overdue_count) AS avg_overdue,
       MAX(overdue_count) AS max_overdue,
       MIN(overdue_count) AS min_overdue
FROM students_groups ssg
JOIN (
    SELECT s.student_id,
           s.group_id,
           COUNT(*) AS overdue_count
    FROM students s
    JOIN assignments_grades ag ON ag.student_id = s.student_id
    JOIN assignments a ON a.assisgnment_id = ag.assisgnment_id
    WHERE ag.date > a.due_date
    GROUP BY s.student_id, s.group_id
) AS overdue_per_student ON overdue_per_student.group_id = ssg.group_id
GROUP BY ssg.group_id;