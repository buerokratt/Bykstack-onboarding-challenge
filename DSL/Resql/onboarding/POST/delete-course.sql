DELETE FROM courses
WHERE course_code = :courseCode
RETURNING 1 AS deleted;
