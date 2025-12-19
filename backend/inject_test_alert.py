import requests
import time
import random

def inject_alert():
    print("Injecting test alert...")
    # Manually trigger the alert callback logic or insert into DB
    # Since we can't easily call the callback from outside, we'll insert into DB directly for the GUI to pick up
    import sqlite3
    import json
    
    conn = sqlite3.connect('incidents.db')
    c = conn.cursor()
    
    fake_details = {
        "Flow Duration": 12345,
        "Total Fwd Packets": 50,
        "Total Backward Packets": 0,
        "Packet Length Mean": 60
    }
    
    c.execute("INSERT INTO incidents (src_ip, dst_ip, type, timestamp, details) VALUES (?, ?, ?, ?, ?)",
              ("192.168.1.105", "8.8.8.8", "DDoS", time.time(), json.dumps(fake_details)))
    conn.commit()
    conn.close()
    print("Test alert injected.")

if __name__ == "__main__":
    inject_alert()
