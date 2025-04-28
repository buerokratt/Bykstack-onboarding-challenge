update courses 
set 
    course_name = COALESCE(:course_name, course_name),
    description = COALESCE(:description, description),
    credits = COALESCE(:credits, credits),
    instructor_id = COALESCE(:instructor_id, instructor_id),
    schedule = CASE 
        WHEN :schedule IS NOT NULL THEN CAST(:schedule AS JSONB)
        ELSE schedule
        END,
    updated_at = CURRENT_TIMESTAMP
where course_code = :course_code
RETURNING
    id, course_code, description, credits, instructor_id, schedule,created_at,updated_at;