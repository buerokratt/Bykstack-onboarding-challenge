-- Enum for student status
CREATE TYPE student_status AS ENUM ('active', 'inactive', 'graduated');

-- Students table
CREATE TABLE students (
id BIGSERIAL PRIMARY KEY,
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
phone VARCHAR(20),
date_of_birth DATE,
gender VARCHAR(10),
enrollment_date DATE NOT NULL,
status student_status DEFAULT 'active',
created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Instructors table
CREATE TABLE instructors (
id BIGSERIAL PRIMARY KEY,
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) NOT NULL,
email VARCHAR(100) UNIQUE NOT NULL,
phone VARCHAR(20),
department VARCHAR(100),
created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Courses table
CREATE TABLE courses (
id BIGSERIAL PRIMARY KEY,
course_code VARCHAR(10) UNIQUE NOT NULL,
course_name VARCHAR(100) NOT NULL,
description TEXT,
credits INT NOT NULL CHECK (credits > 0),
instructor_id BIGINT REFERENCES instructors(id),
schedule JSONB,
created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Enrollments table
CREATE TABLE enrollments (
id BIGSERIAL PRIMARY KEY,
student_id BIGINT NOT NULL REFERENCES students(id),
course_id BIGINT NOT NULL REFERENCES courses(id),
enrollment_date DATE DEFAULT CURRENT_DATE,
status VARCHAR(20) DEFAULT 'active',
UNIQUE (student_id, course_id)
);

-- Attendance table
CREATE TABLE attendance (
id BIGSERIAL PRIMARY KEY,
student_id BIGINT NOT NULL REFERENCES students(id),
course_id BIGINT NOT NULL REFERENCES courses(id),
session_date DATE NOT NULL,
status VARCHAR(10) NOT NULL CHECK (status IN ('present', 'absent', 'late')),
recorded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
UNIQUE (student_id, course_id, session_date)
);

-- Grades table
CREATE TABLE grades (
id BIGSERIAL PRIMARY KEY,
student_id BIGINT NOT NULL REFERENCES students(id),
course_id BIGINT NOT NULL REFERENCES courses(id),
grade VARCHAR(5) NOT NULL,
comments TEXT,
graded_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
UNIQUE (student_id, course_id));
