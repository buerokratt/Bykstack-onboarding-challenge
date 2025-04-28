delete from courses
where course_code = :course_code
RETURNING
    id, course_code, description, credits, instructor_id, schedule, created_at, updated_at;