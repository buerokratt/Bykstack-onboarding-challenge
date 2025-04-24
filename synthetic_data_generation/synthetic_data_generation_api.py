from fastapi import FastAPI, BackgroundTasks, HTTPException, Query
from pydantic import BaseModel
import uvicorn
from typing import Optional, List
import synthetic_data_generation as sdg

app = FastAPI(title="Synthetic Data Generation API")

class SyntheticDataResponse(BaseModel):
    success: bool
    message: str
    inserted_ids: Optional[List[int]] = None
    count: Optional[int] = None


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/generate-students", response_model=SyntheticDataResponse)
async def generate_synthetic_students(
    samples: int = Query(10, description="Number of synthetic samples to generate"),
    limit: int = Query(5, description="Number of records to load from database as reference"),
    host: str = Query("lms-postgres", description="PostgreSQL host"),
    port: int = Query(5432, description="PostgreSQL port"),
    dbname: str = Query("lms_db", description="PostgreSQL database name"),
    user: str = Query("postgres", description="PostgreSQL user"),
    password: str = Query("admin", description="PostgreSQL password"),
    background_tasks: BackgroundTasks = None
):
    """
    Generate synthetic student data and insert it into the database.
    Returns the IDs of inserted students.
    """
    try:
        # Connect to database
        conn = sdg.get_db_connection(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        
        # Load original data from database
        df = sdg.load_student_data(conn, limit)
        
        if len(df) == 0:
            # Create a skeleton dataframe with the expected columns if no data exists
            df = pd.DataFrame(columns=[
                'id', 'first_name', 'last_name', 'email', 'phone', 
                'date_of_birth', 'gender', 'enrollment_date', 'status',
                'created_at', 'updated_at'
            ])
        
        # Generate synthetic data
        synthetic_df = sdg.generate_synthetic_students(df, samples)
        
        # Insert synthetic data into database
        inserted_ids = sdg.insert_students_to_db(conn, synthetic_df)
        
        # Close the database connection
        conn.close()
        
        if inserted_ids:
            return SyntheticDataResponse(
                success=True,
                message=f"Successfully generated and inserted {len(inserted_ids)} synthetic student profiles",
                inserted_ids=inserted_ids,
                count=len(inserted_ids)
            )
        else:
            return SyntheticDataResponse(
                success=False,
                message="No data was inserted",
                inserted_ids=[],
                count=0
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating synthetic data: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("synthetic_data_generation_api:app", host="0.0.0.0", port=9000, reload=True)