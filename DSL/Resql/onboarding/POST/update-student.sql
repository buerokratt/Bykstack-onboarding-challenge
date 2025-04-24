-- name: update-student

UPDATE students
SET
  first_name = COALESCE(:firstName, first_name),
  last_name = COALESCE(:lastName, last_name),
  phone = COALESCE(:phone, phone),
  date_of_birth = COALESCE(:dateOfBirth::date, date_of_birth),
  gender = COALESCE(:gender, gender),
  enrollment_date = COALESCE(:enrollmentDate::date, enrollment_date),
  status = COALESCE((:status)::student_status, status),
  updated_at = COALESCE(:updatedAt::timestamptz, updated_at)
WHERE email = :email;
