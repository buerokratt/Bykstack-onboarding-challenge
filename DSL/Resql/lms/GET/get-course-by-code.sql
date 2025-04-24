SELECT 
    c.id,
    c.course_code,
    c.course_name,
    c.description,
    c.credits,
    c.instructor_id,
    c.schedule,
    c.created_at,
    c.updated_at,
    i.first_name AS instructor_first_name,
    i.last_name AS instructor_last_name,
    i.department AS instructor_department
FROM 
    courses c
LEFT JOIN 
    instructors i ON c.instructor_id = i.id
WHERE 
    c.course_code = :course_code;