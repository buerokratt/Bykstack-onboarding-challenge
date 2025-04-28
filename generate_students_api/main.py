from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, func, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.dialects.postgresql import BIGINT, ENUM
from typing import List, Optional
import datetime
import random
import string
from pydantic import BaseModel
from enum import Enum as PyEnum
import faker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:student@student-postgres:5432/studentdb")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Faker setup
fake = faker.Faker()

# Student Status Enum for Pydantic
class StudentStatus(str, PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    GRADUATED = "graduated"

# SQLAlchemy Student Model
class Student(Base):
    __tablename__ = "students"

    id = Column(BIGINT, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(String(10), nullable=True)
    enrollment_date = Column(Date, nullable=False)
    status = Column(ENUM('active', 'inactive', 'graduated', name='student_status', create_type=False), default='active')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# Pydantic Models
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    date_of_birth: Optional[datetime.date] = None
    gender: Optional[str] = None
    enrollment_date: datetime.date
    status: StudentStatus = StudentStatus.ACTIVE

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True

class GenerateStudentsRequest(BaseModel):
    count: int = 10

class GenerateStudentsResponse(BaseModel):
    generated_count: int
    students: List[StudentResponse]

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Student API", 
              docs_url="/docs")

@app.get("/")
def read_root():
    return {"message": "Student API"}

@app.post("/generate", response_model=GenerateStudentsResponse)
def generate_students(request: GenerateStudentsRequest, db: Session = Depends(get_db)):
    """
    Generate synthetic student data based on existing students in the database.
    This endpoint analyzes patterns from real data and creates new realistic student records.
    """
    # Fetch existing students to analyze patterns
    existing_students = db.query(Student).all()
    
    if not existing_students:
        raise HTTPException(
            status_code=400, 
            detail="Cannot generate synthetic data. No existing students in the database to base patterns on."
        )
    
    # Extract pattern information
    first_names = [student.first_name for student in existing_students]
    last_names = [student.last_name for student in existing_students]
    genders = [student.gender for student in existing_students if student.gender]
    enrollment_dates = [student.enrollment_date for student in existing_students]
    statuses = [student.status for student in existing_students]
    
    # Calculate date ranges
    min_dob = min([student.date_of_birth for student in existing_students if student.date_of_birth], default=datetime.date(2000, 1, 1))
    max_dob = max([student.date_of_birth for student in existing_students if student.date_of_birth], default=datetime.date(2005, 12, 31))
    min_enrollment = min(enrollment_dates, default=datetime.date.today() - datetime.timedelta(days=365*3))
    max_enrollment = max(enrollment_dates, default=datetime.date.today())
    
    # Generate synthetic students
    synthetic_students = []
    generated_emails = set()
    
    for _ in range(request.count):
        # Use patterns from existing data or generate realistic data if insufficient patterns
        first_name = random.choice(first_names) if first_names else fake.first_name()
        last_name = random.choice(last_names) if last_names else fake.last_name()
        
        # Generate a unique email
        email_base = f"{first_name.lower()}.{last_name.lower()}"
        email_suffix = fake.random_element(elements=("@student.edu", "@university.edu", "@college.com"))
        random_digits = ''.join(random.choices(string.digits, k=3))
        email = f"{email_base}{random_digits}{email_suffix}"
        if email in generated_emails:
            # Add random digits to make it unique
            random_digits = ''.join(random.choices(string.digits, k=3))
            email = f"{email_base}{random_digits}{email_suffix}"
        
        generated_emails.add(email)
        
        # Generate other attributes based on patterns
        gender = random.choice(genders) if genders else random.choice(["Male", "Female", "Other", "Prefer not to say"])
        
        # Generate date of birth within the observed range
        dob_range = (max_dob - min_dob).days
        random_days = random.randint(0, dob_range if dob_range > 0 else 365*5)
        date_of_birth = min_dob + datetime.timedelta(days=random_days)
        
        # Generate enrollment date within the observed range
        enrollment_range = (max_enrollment - min_enrollment).days
        random_enrollment_days = random.randint(0, enrollment_range if enrollment_range > 0 else 365)
        enrollment_date = min_enrollment + datetime.timedelta(days=random_enrollment_days)
        
        # Generate phone number
        phone = fake.phone_number()
        if len(phone) > 20:
            phone = phone[:20]
        
        # Choose status with similar distribution to existing data
        status = random.choice(statuses) if statuses else 'active'
        
        # Create new student record
        new_student = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            date_of_birth=date_of_birth,
            gender=gender,
            enrollment_date=enrollment_date,
            status=status
        )
        
        db.add(new_student)
        synthetic_students.append(new_student)
    
    # Commit all new records to the database
    db.commit()
    
    # Refresh to get the generated IDs and timestamps
    for student in synthetic_students:
        db.refresh(student)
    
    return GenerateStudentsResponse(
        generated_count=len(synthetic_students),
        students=synthetic_students
    )

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)