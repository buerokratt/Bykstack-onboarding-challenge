select courses.id, courses.course_code, courses.description, courses.credits, courses.instructor_id, courses.schedule, instructors.first_name as instructors_first_name, instructors.last_name as instructor_last_name, instructors.department as instructor_department from courses 
left join instructors on courses.instructor_id = instructors.id
where courses.course_code = :course_code;