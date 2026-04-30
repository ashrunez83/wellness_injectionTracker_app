#!/bin/bash

echo "Starting Wellness App..."

# Activate virtual environment
source .venv/bin/activate

# Start backend
echo "Starting FastAPI backend..."
cd backend
uvicorn main:app --reload &

# Give backend a second to start
sleep 2

# Start frontend
echo "Starting Streamlit frontend..."
cd ../frontend
streamlit run app.py