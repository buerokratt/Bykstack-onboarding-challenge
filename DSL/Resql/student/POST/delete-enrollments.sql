-- First delete related records in all dependent tables
DELETE FROM enrollments WHERE student_id = :id;
