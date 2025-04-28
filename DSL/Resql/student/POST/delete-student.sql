
-- Then delete the student
DELETE FROM students WHERE id = :id 
RETURNING id, first_name, last_name, gender, email, phone, date_of_birth, enrollment_date, status;
