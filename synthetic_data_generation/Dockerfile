FROM python:3.9-slim

WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the necessary files from synthetic_data_generation folder
COPY synthetic_data_generation.py .
COPY synthetic_data_generation_api.py .

# Expose port for FastAPI
EXPOSE 8000

# Set the default command to run the FastAPI server
CMD ["uvicorn", "synthetic_data_generation_api:app", "--host", "0.0.0.0", "--port", "9000"]