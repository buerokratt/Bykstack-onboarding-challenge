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
FROM
    students
WHERE
    status = COALESCE(CAST(:status AS student_status), status)
ORDER BY
    id ASC
LIMIT CAST(:limit AS INTEGER);