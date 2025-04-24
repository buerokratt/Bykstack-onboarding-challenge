-- name: update-course

UPDATE courses
SET
  course_name = COALESCE(:courseName, course_name),
  description = COALESCE(:description, description),
  credits = COALESCE(:credits, credits),
  instructor_id = COALESCE(:instructorId, instructor_id),
  schedule = CASE 
              WHEN :schedule IS NOT NULL THEN CAST(:schedule AS JSONB)
              ELSE schedule
            END,
  updated_at = CURRENT_TIMESTAMP
WHERE course_code = :courseCode
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