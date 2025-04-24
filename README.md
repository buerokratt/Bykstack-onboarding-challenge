# Bykstack Onboarding Challenge - Learning Management System (LMS)

This project demonstrates a microservices-based Learning Management System built with the Bykstack architecture. The system allows for management of students, courses, and related educational data through a set of containerized services.

## System Architecture

The LMS is composed of the following microservices:

- **Ruuter Public**: API gateway service that handles all external requests
- **ResQL**: SQL query service for database operations
- **PostgreSQL**: Database for storing LMS data
- **Data Mapper**: Service for data transformation and CSV exports
- **S3-Ferry**: Service to transfer files between filesystem and S3 storage
- **Cron Manager**: Scheduler for periodic tasks
- **Synthetic Data Generator**: Creates sample student data for testing

## Features

### Student Management
- Create, read, update, and delete student records
- Export student data to CSV files
- Upload student data to S3 storage

### Course Management
- Create, read, update, and delete course information
- Associate courses with instructors
- Manage course schedules and credits

### Data Generation
- Generate synthetic student profiles for testing
- Schedule automatic data generation using Cron Manager

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Bash shell (for running scripts)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/buerokratt/Bykstack-onboarding-challenge.git
   cd Bykstack-onboarding-challenge
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

3. Initialize the database:
   ```bash
   ./migrate.sh
   ```

### API Endpoints

#### Student APIs
- `POST /lms/students/create` - Create a new student
- `POST /lms/students/update` - Update student information
- `POST /lms/students/delete` - Delete a student
- `GET /lms/students/list` - List all students
- `GET /lms/students/student_to_csv` - Export student data to CSV

#### Course APIs
- `POST /lms/courses/create` - Create a new course
- `POST /lms/courses/update` - Update course information
- `POST /lms/courses/delete` - Delete a course
- `GET /lms/courses/details` - Get course details

### Synthetic Data Generation

Generate synthetic student data using the built-in API:

```bash
curl -X POST "http://localhost:9000/generate-students?samples=10"
```

Or use the scheduled job through Cron Manager:
```bash
docker exec cron-manager python /app/scripts/fetch_students.sh -s 10
```

## Project Structure

```
├── DSL/                      # Domain Specific Language definitions
│   ├── Ruuter.public/        # API gateway definitions (YAML)
│   ├── Resql/                # SQL query definitions
│   ├── Liquibase/            # Database migration scripts
│   ├── DMapper/              # Data transformation templates
│   └── CronManager/          # Scheduled jobs configuration
├── synthetic_data_generation/ # Data generator service
├── constants.ini             # Configuration constants
├── config.env                # Environment variables
├── docker-compose.yml        # Service definitions
└── migrate.sh                # Database migration script
```

## Technologies Used

- **Docker**: Containerization
- **PostgreSQL**: Database
- **Liquibase**: Database migrations
- **FastAPI**: Synthetic data generation API
- **Handlebars**: Template engine for data transformation
- **Bash**: Scripting for automation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
