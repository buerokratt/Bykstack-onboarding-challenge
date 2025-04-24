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
from faker import Faker

# Get database connection parameters from environment variables
DB_HOST = os.getenv("POSTGRES_HOST", "users_db")
DB_PORT = int(os.getenv("POSTGRES_PORT", "5432"))
DB_NAME = os.getenv("POSTGRES_DB", "onboarding")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "rootcode")

fake = Faker('et_EE')


def get_db_connection(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD):
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


def generate_phone_number() -> str:
    return f"+372{random.randint(5000000, 9999999)}"


def generate_synthetic_students(df: pd.DataFrame, num_samples: int = 5) -> pd.DataFrame:
    domains = ["gmail.com", "hotmail.com", "yahoo.com", "mail.ee"]
    genders = df['gender'].unique().tolist() if 'gender' in df.columns else ['male', 'female']
    statuses = df['status'].unique().tolist() if 'status' in df.columns else ['active', 'inactive']

    synthetic_df = pd.DataFrame(columns=df.columns)

    for _ in range(num_samples):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = f"{first_name.lower()}.{last_name.lower()}{random.randint(1000,9999)}@{random.choice(domains)}"
        phone = f"+372{random.randint(5000000, 9999999)}"
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=30).strftime('%Y-%m-%d')
        gender = random.choice(genders)
        enrollment_date = fake.date_between(start_date='-2y', end_date='today').strftime('%Y-%m-%d')
        status = random.choice(statuses)
        current_time = datetime.datetime.now()

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

        filtered_row = {k: v for k, v in new_row.items() if k in df.columns}
        synthetic_df = pd.concat([synthetic_df, pd.DataFrame([filtered_row])], ignore_index=True)

    return synthetic_df


def insert_students_to_db(conn, students_df):
    try:
        cursor = conn.cursor()
        columns = [
            'first_name', 'last_name', 'email', 'phone', 'date_of_birth',
            'gender', 'enrollment_date', 'status'
        ]

        insert_query = f"""
        INSERT INTO students ({', '.join(columns)})
        VALUES %s
        RETURNING id
        """

        values = [
            tuple(row[col] for col in columns)
            for _, row in students_df.iterrows()
        ]

        result = execute_values(cursor, insert_query, values, fetch=True)
        conn.commit()
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

    conn = get_db_connection(
        host=args.host,
        port=args.port,
        dbname=args.dbname,
        user=args.user,
        password=args.password
    )

    print(f"Loading up to {args.limit} students from database as reference data...")
    df = load_student_data(conn, args.limit)

    if len(df) == 0:
        print("No existing student data found. Using default values for synthetic data generation.")
        df = pd.DataFrame(columns=[
            'id', 'first_name', 'last_name', 'email', 'phone', 
            'date_of_birth', 'gender', 'enrollment_date', 'status',
            'created_at', 'updated_at'
        ])

    print(f"Generating {args.samples} synthetic student profiles...")
    synthetic_df = generate_synthetic_students(df, args.samples)

    print("Inserting synthetic data into database...")
    inserted_ids = insert_students_to_db(conn, synthetic_df)

    conn.close()

    if inserted_ids:
        print(f"Successfully generated and inserted {len(inserted_ids)} synthetic student profiles")
        print(f"Inserted student IDs: {', '.join(map(str, inserted_ids))}")
    else:
        print("No data was inserted")


if __name__ == '__main__':
    main()
