#!/bin/bash

# Configuration
SYNTHETIC_DATA_URL="http://synthetic-data:9000/generate-students"

# Function to display usage information
usage() {
  echo "Usage: $0 [-s num_samples]"
  echo "  -s  Number of synthetic samples to generate (default: 10)"
  echo "Example: $0 -s 20"
  exit 1
}

# Process command line arguments
NUM_SAMPLES=10

while getopts "s:" opt; do
  case $opt in
    s) NUM_SAMPLES=$OPTARG ;;
    *) usage ;;
  esac
done

echo "Calling synthetic data generation service to create $NUM_SAMPLES student profiles..."

# Call the synthetic data generation API
RESPONSE=$(curl -s -X POST "$SYNTHETIC_DATA_URL?samples=$NUM_SAMPLES")

# Check if the API call was successful
if [ $? -ne 0 ]; then
  echo "Error: Failed to connect to synthetic data generation service"
  exit 1
fi

# Parse the response
SUCCESS=$(echo "$RESPONSE" | grep -o '"success":[^,}]*' | cut -d':' -f2 | tr -d ' "')
COUNT=$(echo "$RESPONSE" | grep -o '"count":[0-9]*' | cut -d':' -f2)
INSERTED_IDS=$(echo "$RESPONSE" | grep -o '"inserted_ids":\[[^]]*\]' | sed 's/"inserted_ids":\[//;s/\]//')

if [ "$SUCCESS" = "true" ]; then
  echo "SUCCESS: Generated $COUNT synthetic student profiles"
  echo "STUDENT_IDS=$INSERTED_IDS"
else
  echo "ERROR: Failed to generate synthetic data"
  echo "API Response: $RESPONSE"
  exit 1
fi