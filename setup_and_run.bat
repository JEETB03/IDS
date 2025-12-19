@echo off
title Dreadnought IDS - Setup & Run
echo ===================================================
echo      Dreadnought IDS - Deployment Script
echo ===================================================

echo [1/4] Checking Environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed! Please install Python 3.x.
    pause
    exit /b
)
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js is not installed! Please install Node.js.
    pause
    exit /b
)

echo [2/4] Installing Backend Dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install backend dependencies.
    pause
    exit /b
)
cd ..

echo [3/4] Installing Frontend Dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo Failed to install frontend dependencies.
    pause
    exit /b
)
cd ..

echo [4/4] Launching System...
echo Starting Backend Server...
start "Dreadnought Backend" cmd /k "cd backend && python main.py"

echo Starting Frontend Server...
cd frontend
start "Dreadnought Frontend" cmd /k "npm run dev"

echo ===================================================
echo System Deployed! 
echo Dashboard: http://localhost:3000
echo Backend:   http://localhost:8000
echo ===================================================
pause
