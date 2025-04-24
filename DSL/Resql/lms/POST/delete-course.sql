-- name: delete-course

DELETE FROM courses
WHERE course_code = :course_code
RETURNING 
    id,
    course_code,
    course_name,
    description,
    credits,
    instructor_id,
    created_at,
    updated_at;