SELECT
  id,
  first_name,
  last_name,
  email,
  phone,
  date_of_birth,
  gender,
  enrollment_date,
  status,
  created_at,
  updated_at
FROM students
WHERE status != 'inactive'
ORDER BY created_at DESC
LIMIT :page_size OFFSET (:page - 1) * :page_size;
