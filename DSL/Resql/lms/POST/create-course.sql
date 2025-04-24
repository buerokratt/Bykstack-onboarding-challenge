INSERT INTO courses (
    course_code,
    course_name,
    description,
    credits,
    instructor_id,
    schedule
)
VALUES (
    :course_code,
    :course_name,
    :description,
    :credits,
    :instructor_id,
    CAST(:schedule AS JSONB)
)
RETURNING 
    id,
    course_code,
    course_name,
    description,
    credits,
    instructor_id,
    schedule,
    created_at,
    updated_at;