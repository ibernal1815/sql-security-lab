#!/bin/bash

# Start PostgreSQL service if it's not already running
echo "Starting PostgreSQL service..."
sudo systemctl start postgresql

# Check if the service started successfully
if systemctl is-active --quiet postgresql; then
  echo "PostgreSQL is running."
else
  echo "Failed to start PostgreSQL. Check logs for more info."
fi
