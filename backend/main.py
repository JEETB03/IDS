from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sniffer
import threading
import sqlite3
import json
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DB_PATH = "incidents.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS incidents
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  src_ip TEXT, 
                  dst_ip TEXT, 
                  type TEXT, 
                  timestamp REAL, 
                  details TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Global list for real-time dashboard
recent_alerts = []

def alert_callback(alert_data):
    # Save to DB
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO incidents (src_ip, dst_ip, type, timestamp, details) VALUES (?, ?, ?, ?, ?)",
              (alert_data['src_ip'], alert_data['dst_ip'], alert_data['type'], alert_data['timestamp'], json.dumps(alert_data['details'])))
    conn.commit()
    conn.close()
    
    # Update real-time list
    alert_data['time_str'] = datetime.fromtimestamp(alert_data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
    recent_alerts.insert(0, alert_data)
    if len(recent_alerts) > 50:
        recent_alerts.pop()

# Start sniffer in background
@app.on_event("startup")
def startup_event():
    t = threading.Thread(target=sniffer.start_sniffer, args=(alert_callback,))
    t.daemon = True
    t.start()

@app.get("/alerts")
def get_alerts():
    return recent_alerts

@app.get("/stats")
def get_stats():
    return {
        "packets_per_second": sniffer.global_stats["packets_per_second"],
        "total_packets": sniffer.global_stats["total_packets"],
        "active_flows": len(sniffer.active_flows),
        "threat_count": len(recent_alerts) # Or meaningful time-windowed count
    }

@app.get("/history")
def get_history():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM incidents ORDER BY timestamp DESC LIMIT 1000")
    rows = c.fetchall()
    conn.close()
    
    history = []
    for row in rows:
        history.append({
            "id": row[0],
            "src_ip": row[1],
            "dst_ip": row[2],
            "type": row[3],
            "timestamp": row[4],
            "time_str": datetime.fromtimestamp(row[4]).strftime('%Y-%m-%d %H:%M:%S'),
            "details": json.loads(row[5])
        })
    return history

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
