get_ini_value() {
    local file=$1
    local key=$2
    awk -F '=' -v key="$key" '$1 == key { gsub(/^[ \t]+|[ \t]+$/, "", $2); print $2; exit }' "$file"
}

INI_FILE="constants.ini"
DB_PASSWORD=$(get_ini_value "$INI_FILE" "DB_PASSWORD")


docker run --rm --network obcnet -v `pwd`/DSL/Liquibase/changelog:/liquibase/changelog -v `pwd`/DSL/Liquibase/master.yml:/liquibase/master.yml -v `pwd`/DSL/Liquibase/data:/liquibase/data liquibase/liquibase --defaultsFile=/liquibase/changelog/liquibase.properties --changelog-file=master.yml --url=jdbc:postgresql://student-postgres:5432/studentdb?user=postgres --password=$DB_PASSWORD update