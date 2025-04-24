INSERT INTO students (
    first_name,
    last_name,
    email,
    phone,
    date_of_birth,
    gender,
    enrollment_date,
    status
)
VALUES (
    :first_name,
    :last_name,
    :email,
    :phone,
    CASE WHEN :date_of_birth = '' OR :date_of_birth IS NULL THEN NULL ELSE :date_of_birth::DATE END,
    :gender,
    :enrollment_date::DATE,
    :status::student_status
)
RETURNING 
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
    updated_at;