UPDATE students

SET 
    first_name = COALESCE(:optional_first_name, first_name),
    last_name = COALESCE(:optional_last_name, last_name),
    phone = COALESCE(:optional_phone, phone),
    email = COALESCE(:optional_email, email),
    date_of_birth = COALESCE(CAST(:optional_date_of_birth AS date), date_of_birth),
    status = COALESCE(CAST(:optional_student_status AS student_status), status),
    updated_at = CURRENT_TIMESTAMP
WHERE id = :id;