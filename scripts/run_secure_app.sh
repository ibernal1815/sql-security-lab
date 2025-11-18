#!/bin/bash

source ../venv/bin/activate
export FLASK_APP=secure_app.py
export FLASK_ENV=development

echo "Running Secure App..."
flask run --host=0.0.0.0 --port=5001
