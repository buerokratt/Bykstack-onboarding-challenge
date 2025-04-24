UPDATE courses
SET
  course_name = COALESCE(:courseName, course_name),
  description = COALESCE(:description, description),
  credits = COALESCE(:credits, credits),
  instructor_id = COALESCE(:instructorId, instructor_id),
  schedule = COALESCE(CAST(:schedule AS JSONB), schedule),
  updated_at = :updatedAt::timestamp with time zone
WHERE course_code = :courseCode
RETURNING 1 AS updated;
