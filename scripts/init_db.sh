#!/bin/bash

# Exit on any error
set -e

# Navigate to the script directory
cd "$(dirname "$0")"

# Run roles setup
echo "Creating roles..."
psql -U postgres -f ../database/roles.sql

# Run schema setup
echo "Creating schema..."
psql -U sql_admin -d sql_lab -f ../database/schema.sql

# Run seed data
echo "Seeding database..."
psql -U sql_admin -d sql_lab -f ../database/seed_data.sql

echo "Database initialized successfully."
