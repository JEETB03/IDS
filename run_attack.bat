@echo off
title Dreadnought IDS - Attack Simulation
echo ===================================================
echo      Dreadnought IDS - Attack Simulation
echo ===================================================

echo Launching Attack Simulation...
cd backend
python attack_sim.py

echo.
echo Simulation Complete. Check the Dashboard for alerts.
pause
