#!/bin/bash

echo "==================================================="
echo "      Dreadnought IDS - Attack Simulation"
echo "==================================================="

echo "Launching Attack Simulation..."
cd backend
python3 attack_sim.py

echo ""
echo "Simulation Complete. Check the Dashboard for alerts."
