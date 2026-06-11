-- Ученики учителя с максимальным средним баллом по его заданиям
-- (подзапросы и JOIN)
SELECT DISTINCT s.student_id,
       s.full_name
FROM students s
JOIN assignments_grades ag ON ag.student_id = s.student_id
JOIN assignments a ON a.assisgnment_id = ag.assisgnment_id
JOIN teachers t ON t.teacher_id = a.teacher_id
-- в WHERE указываем, что teacher_id = teacher_id с максимальным средним
WHERE a.teacher_id = (
    SELECT a2.teacher_id
    FROM assignments a2
    JOIN assignments_grades ag2 ON ag2.assisgnment_id = a2.assisgnment_id
    GROUP BY a2.teacher_id
    ORDER BY AVG(ag2.grade) DESC
    LIMIT 1
);