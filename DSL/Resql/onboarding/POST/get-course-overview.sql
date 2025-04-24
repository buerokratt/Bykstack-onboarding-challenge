SELECT
  course_code,
  course_name,
  description,
  credits,
  instructor_id,
  schedule,
  created_at,
  updated_at
FROM courses
WHERE course_code = :courseCode;
