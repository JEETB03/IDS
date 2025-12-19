import scapy.all as scapy
from scapy.layers.inet import TCP, UDP, IP
import numpy as np
import pandas as pd
import time
import threading
import joblib
import os
from collections import defaultdict

# Configuration
MODEL_PATH = "model.pkl"
SCALER_PATH = "scaler.pkl"
FEATURES_PATH = "selected_features.pkl"
LABEL_ENCODER_PATH = "label_encoder.pkl"

class Flow:
    def __init__(self, src_ip, dst_ip, src_port, dst_port, protocol):
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        self.protocol = protocol
        self.start_time = time.time()
        self.last_seen = time.time()
        self.packets = []
        self.fwd_packets = 0
        self.bwd_packets = 0
        self.fwd_bytes = 0
        self.bwd_bytes = 0
        self.lengths = []
        self.iat = []
        
    def add_packet(self, packet, direction):
        current_time = time.time()
        if self.packets:
            self.iat.append(current_time - self.last_seen)
        self.last_seen = current_time
        self.packets.append(packet)
        
        length = len(packet)
        self.lengths.append(length)
        
        if direction == "fwd":
            self.fwd_packets += 1
            self.fwd_bytes += length
        else:
            self.bwd_packets += 1
            self.bwd_bytes += length

    def get_features(self):
        duration = self.last_seen - self.start_time
        if duration == 0: duration = 1e-6 # Avoid division by zero
        
        mean_len = np.mean(self.lengths) if self.lengths else 0
        std_len = np.std(self.lengths) if self.lengths else 0
        max_len = np.max(self.lengths) if self.lengths else 0
        min_len = np.min(self.lengths) if self.lengths else 0
        
        mean_iat = np.mean(self.iat) if self.iat else 0
        std_iat = np.std(self.iat) if self.iat else 0
        max_iat = np.max(self.iat) if self.iat else 0
        min_iat = np.min(self.iat) if self.iat else 0
        
        flow_bytes_s = (self.fwd_bytes + self.bwd_bytes) / duration
        flow_packets_s = (self.fwd_packets + self.bwd_packets) / duration
        
        # Mapping to CICIDS2017 feature names (approximate)
        features = {
            "Destination Port": self.dst_port,
            "Flow Duration": duration * 1e6, # Microseconds
            "Total Fwd Packets": self.fwd_packets,
            "Total Backward Packets": self.bwd_packets,
            "Total Length of Fwd Packets": self.fwd_bytes,
            "Total Length of Bwd Packets": self.bwd_bytes,
            "Fwd Packet Length Max": max_len, # Simplified
            "Fwd Packet Length Min": min_len, # Simplified
            "Fwd Packet Length Mean": mean_len, # Simplified
            "Fwd Packet Length Std": std_len, # Simplified
            "Bwd Packet Length Max": max_len, # Simplified
            "Bwd Packet Length Min": min_len, # Simplified
            "Bwd Packet Length Mean": mean_len, # Simplified
            "Bwd Packet Length Std": std_len, # Simplified
            "Flow Bytes/s": flow_bytes_s,
            "Flow Packets/s": flow_packets_s,
            "Flow IAT Mean": mean_iat * 1e6,
            "Flow IAT Std": std_iat * 1e6,
            "Flow IAT Max": max_iat * 1e6,
            "Flow IAT Min": min_iat * 1e6,
            "Fwd IAT Total": 0, # Placeholder
            "Fwd IAT Mean": 0, # Placeholder
            "Fwd IAT Std": 0, # Placeholder
            "Fwd IAT Max": 0, # Placeholder
            "Fwd IAT Min": 0, # Placeholder
            "Bwd IAT Total": 0, # Placeholder
            "Bwd IAT Mean": 0, # Placeholder
            "Bwd IAT Std": 0, # Placeholder
            "Bwd IAT Max": 0, # Placeholder
            "Bwd IAT Min": 0, # Placeholder
            "Fwd PSH Flags": 0,
            "Bwd PSH Flags": 0,
            "Fwd URG Flags": 0,
            "Bwd URG Flags": 0,
            "Fwd Header Length": 0,
            "Bwd Header Length": 0,
            "Fwd Packets/s": self.fwd_packets / duration,
            "Bwd Packets/s": self.bwd_packets / duration,
            "Min Packet Length": min_len,
            "Max Packet Length": max_len,
            "Packet Length Mean": mean_len,
            "Packet Length Std": std_len,
            "Packet Length Variance": std_len ** 2,
            "FIN Flag Count": 0,
            "SYN Flag Count": 0,
            "RST Flag Count": 0,
            "PSH Flag Count": 0,
            "ACK Flag Count": 0,
            "URG Flag Count": 0,
            "CWE Flag Count": 0,
            "ECE Flag Count": 0,
            "Down/Up Ratio": 0,
            "Average Packet Size": mean_len,
            "Avg Fwd Segment Size": mean_len,
            "Avg Bwd Segment Size": mean_len,
            "Fwd Header Length.1": 0,
            "Fwd Avg Bytes/Bulk": 0,
            "Fwd Avg Packets/Bulk": 0,
            "Fwd Avg Bulk Rate": 0,
            "Bwd Avg Bytes/Bulk": 0,
            "Bwd Avg Packets/Bulk": 0,
            "Bwd Avg Bulk Rate": 0,
            "Subflow Fwd Packets": self.fwd_packets,
            "Subflow Fwd Bytes": self.fwd_bytes,
            "Subflow Bwd Packets": self.bwd_packets,
            "Subflow Bwd Bytes": self.bwd_bytes,
            "Init_Win_bytes_forward": 0,
            "Init_Win_bytes_backward": 0,
            "act_data_pkt_fwd": 0,
            "min_seg_size_forward": 0,
            "Active Mean": 0,
            "Active Std": 0,
            "Active Max": 0,
            "Active Min": 0,
            "Idle Mean": 0,
            "Idle Std": 0,
            "Idle Max": 0,
            "Idle Min": 0,
        }
        return features

active_flows = {}
flow_lock = threading.Lock()
flow_timeout = 5 # Seconds

def packet_callback(packet):
    if not packet.haslayer(IP):
        return

    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    protocol = packet[IP].proto
    
    src_port = 0
    dst_port = 0
    
    if packet.haslayer(TCP):
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
    elif packet.haslayer(UDP):
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
        
    flow_id = (src_ip, dst_ip, src_port, dst_port, protocol)
    reverse_flow_id = (dst_ip, src_ip, dst_port, src_port, protocol)
    
    with flow_lock:
        if flow_id in active_flows:
            active_flows[flow_id].add_packet(packet, "fwd")
        elif reverse_flow_id in active_flows:
            active_flows[reverse_flow_id].add_packet(packet, "bwd")
        else:
            active_flows[flow_id] = Flow(src_ip, dst_ip, src_port, dst_port, protocol)
            active_flows[flow_id].add_packet(packet, "fwd")

def process_flows(callback_func):
    model = None
    scaler = None
    selected_features = None
    label_encoder = None
    
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        selected_features = joblib.load(FEATURES_PATH)
        label_encoder = joblib.load(LABEL_ENCODER_PATH)
        print("Model loaded.")
    else:
        print("Model not found. Waiting for training...")
    
    while True:
        current_time = time.time()
        to_remove = []
        
        # Use lock when iterating
        with flow_lock:
            # Create a copy of items to iterate safely if we were just reading, 
            # but since we might modify or just read, holding lock is safest for now.
            # However, holding lock for entire prediction might block sniffer.
            # Better: Identify flows to process, then process them outside lock?
            # For simplicity and correctness now:
            
            # We need to iterate to find timed out flows
            # We can iterate over a copy of keys/items
            snapshot = list(active_flows.items())
        
        for flow_id, flow in snapshot:
            if current_time - flow.last_seen > flow_timeout:
                # Flow finished, extract features and predict
                features = flow.get_features()
                to_remove.append(flow_id)
                
                if model and selected_features:
                    try:
                        # Prepare dataframe
                        df = pd.DataFrame([features])
                        # Filter features
                        X = df[selected_features]
                        # Scale
                        X = scaler.transform(X)
                        # Predict
                        prediction = model.predict(X)[0]
                        label = label_encoder.inverse_transform([prediction])[0]
                        
                        # Debug print
                        print(f"Flow {flow.src_ip} -> {flow.dst_ip} : {label}")
                        
                        # Heuristic Fallback for Demo/Simulation
                        if label == "BENIGN" and flow.fwd_packets > 100:
                            label = "DDoS"
                            print(f"Heuristic Alert: DDoS detected from {flow.src_ip}")

                        if label != "BENIGN":
                            print(f"ALERT: {label} detected from {flow.src_ip} to {flow.dst_ip}")
                            
                            # Convert numpy types to python types for JSON serialization
                            serializable_features = {k: int(v) if isinstance(v, (np.integer, np.int32, np.int64)) else float(v) if isinstance(v, (np.floating, np.float32, np.float64)) else v for k, v in features.items()}
                            
                            callback_func({
                                "src_ip": flow.src_ip,
                                "dst_ip": flow.dst_ip,
                                "type": label,
                                "timestamp": current_time,
                                "details": serializable_features
                            })
                    except Exception as e:
                        print(f"Prediction error: {e}")
        
        if to_remove:
            with flow_lock:
                for flow_id in to_remove:
                    if flow_id in active_flows:
                        del active_flows[flow_id]
            
        time.sleep(1)

def start_sniffer(callback_func):
    t = threading.Thread(target=process_flows, args=(callback_func,))
    t.daemon = True
    t.start()
    
    print("Starting sniffer...")
    scapy.sniff(prn=packet_callback, store=False)
