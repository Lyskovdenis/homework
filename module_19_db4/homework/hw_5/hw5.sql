-- 5. Анализ групп (классов)
SELECT ssg.group_id,
       COUNT(avg_stats.student_id) AS students_count,
       AVG(avg_stats.avg_grade) AS avg_grade_group,
       SUM(CASE WHEN avg_stats.has_submitted = 0 THEN 1 ELSE 0 END) AS students_not_submitted,
       SUM(CASE WHEN avg_stats.has_overdue = 1 THEN 1 ELSE 0 END) AS students_overdue,
       SUM(CASE WHEN avg_stats.submissions_count > 1 THEN 1 ELSE 0 END) AS students_with_retries
FROM students_groups ssg
JOIN (
    SELECT s.student_id,
           s.group_id,
           AVG(ag.grade) AS avg_grade,
           CASE WHEN SUM(CASE WHEN ag.grade IS NOT NULL THEN 1 ELSE 0 END) > 0 THEN 1 ELSE 0 END AS has_submitted,
           CASE WHEN SUM(CASE WHEN ag.date > a.due_date THEN 1 ELSE 0 END) > 0 THEN 1 ELSE 0 END AS has_overdue,
           COUNT(*) AS submissions_count
    FROM students s
    JOIN assignments_grades ag ON ag.student_id = s.student_id
    JOIN assignments a ON a.assisgnment_id = ag.assisgnment_id
    GROUP BY s.student_id, s.group_id
) avg_stats ON avg_stats.group_id = ssg.group_id
GROUP BY ssg.group_id;