#!/bin/bash

echo "==================================================="
echo "      Dreadnought IDS - Deployment Script"
echo "==================================================="

echo "[1/4] Checking Environment..."
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed!"
    exit 1
fi
if ! command -v node &> /dev/null; then
    echo "Node.js is not installed!"
    exit 1
fi

echo "[2/4] Installing Backend Dependencies..."
cd backend
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install backend dependencies."
    exit 1
fi
cd ..

echo "[3/4] Installing Frontend Dependencies..."
cd frontend
npm install
if [ $? -ne 0 ]; then
    echo "Failed to install frontend dependencies."
    exit 1
fi
cd ..

echo "[4/4] Launching System..."
echo "Starting Backend Server..."
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

echo "Starting Frontend Server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "==================================================="
echo "System Deployed!"
echo "Dashboard: http://localhost:3000"
echo "Backend:   http://localhost:8000"
echo "Press Ctrl+C to stop all services."
echo "==================================================="

trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT
wait
