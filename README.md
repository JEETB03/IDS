
# Dreadnought IDS - Network Intrusion Detection System

## 🛡️ Overview
Dreadnought IDS is a powerful, real-time Network Intrusion Detection System (IDS) that leverages Machine Learning to detect malicious network traffic. It combines packet sniffing with a trained XGBoost model to classify network flows as benign or malicious (e.g., DDoS, Port Scans). The system features a modern, reactive web dashboard for monitoring network health and alerts.

## ✨ Features
*   **Real-time Traffic Monitoring**: Captures and analyzes network packets on the fly.
*   **ML-Powered Detection**: Uses a pre-trained XGBoost model to identify anomalies.
*   **Heuristic Fallback**: Includes rule-based heuristics for high-speed attacks like Port Scans and massive DDoS that might slip past flow-based ML or require immediate flagging.
*   **Modern Dashboard**: A Next.js 15 + Tailwind CSS frontend visualizing network load, active flows, and threat intensity.
*   **Dynamic Visualization**: Interactive charts that react to attack intensity; UI flashes red during active threats.
*   **Detailed Logging**: SQlite-backed incident logging for forensic review.

## 🏗️ Architecture
The system consists of two main components:
1.  **Backend (Python/FastAPI)**:
    *   `sniffer.py`: captured packets using `scapy`, extracts features (CICIDS2017 compliant), and aggregates them into flows.
    *   `main.py`: FastAPI server exposing endpoints for alerts (`/alerts`) and statistics (`/stats`).
    *   `model.pkl`: The XGBoost classification model.
2.  **Frontend (Next.js/React)**:
    *   Real-time dashboard polling the backend.
    *   Visualizes Threat Intensity vs Traffic Volume.
    *   Displays detailed alert logs.

## 🚀 Getting Started

### Prerequisites
*   **Python 3.8+** (with pip)
*   **Node.js 18+** (with npm)
*   **Npcap** (Required for Scapy on Windows) or `libpcap` (Linux)

### Installation
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/JEETB03/IDS.git
    cd IDS
    ```
2.  **Run Setup Script**:
    We provide an automated script to install all dependencies and start the system.
    *   **Windows**: Double-click `setup_and_run.bat` or run:
        ```cmd
        setup_and_run.bat
        ```
    *   **Linux/Mac**:
        ```bash
        chmod +x setup_and_run.sh
        ./setup_and_run.sh
        ```

### Manual Setup (If script fails)
1.  **Backend**:
    ```bash
    cd backend
    pip install -r requirements.txt
    python main.py
    ```
2.  **Frontend**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

## 🧪 Testing & Simulation
The project includes tools to simulate attacks for testing purposes.

### 1. DDoS Simulation (SYN Flood)
Simulates a classic high-volume SYN flood attack.
```bash
cd backend
python attack_sim.py
```
*   **Effect**: Generates massive traffic volume.
*   **Detection**: Should trigger "DDoS" alerts in the dashboard and cause the graph to spike.

### 2. Port Scan Simulation
Simulates a rapid port scanning attempt.
```bash
cd backend
python port_scan_sim.py
```
*   **Effect**: Rapidly attempts to connect to sequential ports on a target.
*   **Detection**: Should trigger "Port Scan" heuristic alerts.

## 📊 Dashboard Guide
*   **System Status**: Shows "Active Monitoring" (Green) or "Under Attack" (Red).
*   **Stats**:
    *   **Active Flows**: Number of currently tracked network connections.
    *   **Traffic (PPS)**: Packets Per Second processed by the sniffer.
    *   **Threats Detected**: Total threats found since startup.
*   **Graph**: 
    *   **Purple Line**: Traffic volume (PPS).
    *   **Red Line**: Threat intensity.

## 📂 Project Structure
```
Dreadnought-IDS/
├── backend/                # Python Backend
│   ├── main.py             # API Server
│   ├── sniffer.py          # Packet Capture & ML Inference
│   ├── attack_sim.py       # DDoS Simulator
│   ├── port_scan_sim.py    # Port Scan Simulator
│   ├── model.pkl           # Trained ML Model
│   └── ...
├── frontend/               # Next.js Frontend
│   ├── app/                # Pages & Layouts
│   ├── components/         # React Components (Dashboard, Charts)
│   └── ...
├── setup_and_run.bat       # Windows Setup Script
└── README.md
```

## ⚠️ Disclaimer
This tool is for **EDUCATIONAL AND DEFENSIVE TESTING PURPOSES ONLY**. Do not use the included attack simulators on networks you do not own or have explicit permission to test.
