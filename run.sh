#!/bin/bash
echo 'Starting Water Intake Tracker Server Application...'
export PYTHONPATH=./src


echo "About to run Server App's API is running at: http://127.0.0.1:8000"
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

echo 'Uvicorn server stopped or exited'
