SELECT t.teacher_id,
       t.full_name,
       AVG(ag.grade) AS avg_grade
FROM teachers t
JOIN students_groups sg ON sg.teacher_id = t.teacher_id
JOIN students st ON st.group_id = sg.group_id
JOIN assignments_grades ag ON ag.student_id = st.student_id
JOIN assignments a ON a.assisgnment_id = ag.assisgnment_id
WHERE a.teacher_id = t.teacher_id
GROUP BY t.teacher_id, t.full_name
HAVING AVG(ag.grade) = (
    SELECT MIN(avg_by_teacher)
    FROM (
        SELECT t2.teacher_id, AVG(ag2.grade) AS avg_by_teacher
        FROM teachers t2
        JOIN students_groups sg2 ON sg2.teacher_id = t2.teacher_id
        JOIN students st2 ON st2.group_id = sg2.group_id
        JOIN assignments_grades ag2 ON ag2.student_id = st2.student_id
        JOIN assignments a2 ON a2.assisgnment_id = ag2.assisgnment_id
        WHERE a2.teacher_id = t2.teacher_id
        GROUP BY t2.teacher_id
    ) AS sub
);