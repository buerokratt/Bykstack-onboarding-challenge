UPDATE students
SET
  status = (:status)::student_status,
  updated_at = :updatedAt::timestamptz
WHERE email = :email;
