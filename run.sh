#!/bin/bash

# Run both backend and frontend for Big Shot on macOS & Linux

echo "Starting Big Shot Application..."

# Start backend API in the background
echo "Starting backend..."
python3 api.py &
BACKEND_PID=$!

# Give backend a moment to start
sleep 2

# Start frontend in the background
echo "Starting frontend..."
python3 main.py &
FRONTEND_PID=$!

echo "Both services starting..."
echo "Backend: http://localhost:8000"
echo "Frontend: Will open automatically (if applicable)"

# Optional: Wait for both processes to finish
wait $BACKEND_PID $FRONTEND_PID
