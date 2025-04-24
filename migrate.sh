#!/bin/bash

# Path to constants.ini file
INI_FILE="$(dirname "$0")/constants.ini"

# Function to parse ini file and extract the value from a specific section
get_ini_value() {
    local file=$1
    local section=$2
    local key=$3
    local value

    # Check if file exists
    if [ ! -f "$file" ]; then
        echo "Error: INI file not found: $file" >&2
        return 1
    fi
    
    # Extract value using awk
    value=$(awk -F '=' -v section="[$section]" -v key="$key" '
        # Track current section
        /^\[.*\]/ { current_section = $0; next }
        # If in the right section and matching key
        current_section == section && $1 ~ "^[[:space:]]*" key "[[:space:]]*$" { 
            # Extract value and remove leading/trailing whitespace
            value = $2
            gsub(/^[ \t]+|[ \t]+$/, "", value)
            print value
            exit
        }
    ' "$file")
    
    # Check if value was found
    if [ -z "$value" ]; then
        echo "Warning: Key '$key' not found in section '$section' of $file" >&2
        return 1
    fi
    
    echo "$value"
}

echo "Reading configuration from $INI_FILE..."

# Extract values from constants.ini
DB_PASSWORD=$(get_ini_value "$INI_FILE" "DSL" "DB_PASSWORD")

# Display extracted values (remove this in production for security)
echo "Database Password: $DB_PASSWORD"

# Use the extracted values in your docker run command
docker run --rm --network lmsnet \
    -v `pwd`/DSL/Liquibase/changelog:/liquibase/changelog \
    -v `pwd`/DSL/Liquibase/master.yml:/liquibase/master.yml \
    -v `pwd`/DSL/Liquibase/data:/liquibase/data \
    liquibase/liquibase \
    --defaultsFile=/liquibase/changelog/liquibase.properties \
    --changelog-file=master.yml \
    --url=jdbc:postgresql://lms-postgres:5432/lms_db?user=postgres \
    --password=$DB_PASSWORD update