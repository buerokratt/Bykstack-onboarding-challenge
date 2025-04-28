echo "Starting student generation script..."

# url for the student generation API
url="http://172.25.0.15:8000/generate"


RESPONSE=$(curl  -X POST "$url" -H "Content-Type: application/json" -d '{
    "count": 10
}')

# check if the call was successful
if [ $? -eq 0 ]; then
    echo "Student generation request sent successfully."
else
    echo "Failed to send student generation request."
    exit 1
fi

