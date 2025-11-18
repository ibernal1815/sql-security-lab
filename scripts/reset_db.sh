#!/bin/bash

# Exit on any error
set -e

# Navigate to the project root
cd "$(dirname "$0")"

echo "Dropping database..."
psql -U postgres -c "DROP DATABASE IF EXISTS sql_lab;"

echo "Creating fresh database..."
psql -U postgres -c "CREATE DATABASE sql_lab OWNER sql_admin;"

# Reinitialize roles, schema, and seed
./init_db.sh

echo "Database reset complete."
