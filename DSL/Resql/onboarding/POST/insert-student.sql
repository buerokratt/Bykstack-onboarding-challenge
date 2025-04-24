INSERT INTO students (
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
)
VALUES (
    :firstName,
    :lastName,
    :email,
    :phone,
    :dateOfBirth::date,
    :gender,
    :enrollmentDate::date,
    (:status)::student_status,
    :createdAt::timestamp with time zone,
    :updatedAt::timestamp with time zone
);
