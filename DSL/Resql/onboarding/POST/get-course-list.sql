SELECT
  id,
  course_code,
  course_name,
  description,
  credits,
  instructor_id,
  schedule,
  created_at,
  updated_at
FROM courses
ORDER BY created_at DESC
LIMIT :pageSize OFFSET (:page - 1) * :pageSize;
