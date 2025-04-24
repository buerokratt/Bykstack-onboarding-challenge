import pandas as pd
import numpy as np
import argparse
import datetime
import json
import os
import random
from typing import List, Dict
import sys
import psycopg2
from psycopg2.extras import execute_values
from constants import *

def get_db_connection(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD):
    """Create a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {str(e)}")
        sys.exit(1)

def load_student_data(db_conn=None, limit=100) -> pd.DataFrame:
    """Load student data from PostgreSQL database."""
    try:
        if db_conn is None:
            db_conn = get_db_connection()
            
        query = f"""
        SELECT 
            id, first_name, last_name, email, phone, 
            date_of_birth, gender, enrollment_date, status,
            created_at, updated_at
        FROM students
        ORDER BY id
        LIMIT {limit}
        """
        
        df = pd.read_sql_query(query, db_conn)
        return df
    except Exception as e:
        print(f"Error loading student data: {str(e)}")
        sys.exit(1)

def generate_synthetic_students(df: pd.DataFrame, num_samples: int = 5) -> pd.DataFrame:
    """Generate synthetic student data based on patterns in the input data."""
    # Define more diverse lists of first and last names
    estonian_first_names = ESTONIAN_FIRST_NAMES
    
    estonian_last_names = ESTONIAN_LAST_NAMES
    
    # Use provided names if available, otherwise use our diverse lists
    first_names = df['first_name'].unique().tolist() if ('first_name' in df.columns and len(df['first_name'].unique()) > 5) else estonian_first_names
    last_names = df['last_name'].unique().tolist() if ('last_name' in df.columns and len(df['last_name'].unique()) > 5) else estonian_last_names
    
    # Ensure we have the other categorical fields
    genders = df['gender'].unique().tolist() if 'gender' in df.columns else ['male', 'female']
    statuses = df['status'].unique().tolist() if 'status' in df.columns else ['active', 'inactive']
    
    # Create empty dataframe with same columns
    synthetic_df = pd.DataFrame(columns=df.columns)
    
    # Generate synthetic students
    for i in range(num_samples):
        # Generate random first and last names
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        # Generate random email with unique suffix to avoid duplicates
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(100, 9999)}@example.com"
        
        # Generate random phone number (Estonian format)
        phone = f"+372{random.randint(5000000, 9999999)}"
        
        # Generate random date of birth (18-30 years ago)
        years_ago = random.randint(18, 30)
        dob = (datetime.datetime.now() - datetime.timedelta(days=365*years_ago + random.randint(0, 364)))
        date_of_birth = dob.strftime('%Y-%m-%d')
        
        # Generate random gender
        gender = random.choice(genders)
        
        # Generate random enrollment date (within last 1-2 years)
        days_ago = random.randint(30, 730)
        enrollment = (datetime.datetime.now() - datetime.timedelta(days=days_ago))
        enrollment_date = enrollment.strftime('%Y-%m-%d')
        
        # Generate random status
        status = random.choice(statuses)
        
        # Generate creation and update timestamps
        current_time = datetime.datetime.now()
        
        # Create new row
        new_row = {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'date_of_birth': date_of_birth,
            'gender': gender,
            'enrollment_date': enrollment_date,
            'status': status,
            'created_at': current_time,
            'updated_at': current_time
        }
        
        # Only include columns that are in the original dataframe
        filtered_row = {k: v for k, v in new_row.items() if k in df.columns}
        synthetic_df = pd.concat([synthetic_df, pd.DataFrame([filtered_row])], ignore_index=True)
    
    return synthetic_df

def insert_students_to_db(conn, students_df):
    """Insert synthetic student data into PostgreSQL database."""
    try:
        cursor = conn.cursor()
        
        # Define the columns that we want to insert
        columns = [
            'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
            'gender', 'enrollment_date', 'status'
        ]
        
        # Prepare the SQL statement
        insert_query = f"""
        INSERT INTO students ({', '.join(columns)})
        VALUES %s
        RETURNING id
        """
        
        # Convert dataframe to list of tuples for execute_values
        values = []
        for _, row in students_df.iterrows():
            values.append((
                row['first_name'],
                row['last_name'],
                row['email'],
                row['phone'],
                row['date_of_birth'],
                row['gender'],
                row['enrollment_date'],
                row['status']
            ))
        
        # Execute the query with all values
        result = execute_values(cursor, insert_query, values, fetch=True)
        
        # Commit the transaction
        conn.commit()
        
        # Return the IDs of the inserted rows
        return [r[0] for r in result]
    
    except Exception as e:
        conn.rollback()
        print(f"Error inserting data: {str(e)}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Generate synthetic student data')
    parser.add_argument('--host', default='lms-postgres', help='PostgreSQL host')
    parser.add_argument('--port', type=int, default=5432, help='PostgreSQL port')
    parser.add_argument('--dbname', default='lms_db', help='PostgreSQL database name')
    parser.add_argument('--user', default='postgres', help='PostgreSQL user')
    parser.add_argument('--password', default='admin', help='PostgreSQL password')
    parser.add_argument('--samples', '-s', type=int, default=5, help='Number of synthetic samples to generate')
    parser.add_argument('--limit', '-l', type=int, default=100, help='Number of records to load from database as reference')
    
    args = parser.parse_args()
    
    # Connect to database
    conn = get_db_connection(
        host=args.host,
        port=args.port,
        dbname=args.dbname,
        user=args.user,
        password=args.password
    )
    
    # Load original data from database
    print(f"Loading up to {args.limit} students from database as reference data...")
    df = load_student_data(conn, args.limit)
    
    if len(df) == 0:
        print("No existing student data found. Using default values for synthetic data generation.")
        # Create a skeleton dataframe with the expected columns
        df = pd.DataFrame(columns=[
            'id', 'first_name', 'last_name', 'email', 'phone', 
            'date_of_birth', 'gender', 'enrollment_date', 'status',
            'created_at', 'updated_at'
        ])
    
    # Generate synthetic data
    print(f"Generating {args.samples} synthetic student profiles...")
    synthetic_df = generate_synthetic_students(df, args.samples)
    
    # Insert synthetic data into database
    print("Inserting synthetic data into database...")
    inserted_ids = insert_students_to_db(conn, synthetic_df)
    
    # Close the database connection
    conn.close()
    
    if inserted_ids:
        print(f"Successfully generated and inserted {len(inserted_ids)} synthetic student profiles")
        print(f"Inserted student IDs: {', '.join(map(str, inserted_ids))}")
    else:
        print("No data was inserted")