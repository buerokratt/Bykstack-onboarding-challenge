-- name: get-students

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
    email = :email;