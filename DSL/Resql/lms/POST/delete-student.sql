DELETE FROM students
WHERE id = :student_id
RETURNING 
    id,
    first_name,
    last_name,
    email,
    status;