#!/bin/bash

source ../venv/bin/activate
export FLASK_APP=vulnerable_app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

echo "Running Vulnerable App..."
flask run --host=0.0.0.0 --port=5000
