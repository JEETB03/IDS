
import scapy.all as scapy
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import Ether
import random
import time

def port_scan(target_ip, start_port=1, end_port=1003):
    print(f"Starting Port Scan simulation on {target_ip} from {start_port} to {end_port}...")
    
    # Use local IP as source to ensure outgoing packets are captured
    src_ip = "192.168.0.107" 
    src_port = 54321
    
    for port in range(start_port, end_port):
        # Create packet
        eth = Ether(dst="ff:ff:ff:ff:ff:ff")
        ip = IP(src=src_ip, dst=target_ip)
        tcp = TCP(sport=src_port, dport=port, flags="S")
        packet = eth / ip / tcp
        
        # Send at Layer 2
        scapy.sendp(packet, verbose=False)
        
        if port % 100 == 0:
            print(f"Scanned port {port}...")
            time.sleep(0.01) # Small delay to not overwhelm immediately
            
    print("Port Scan simulation completed.")

if __name__ == "__main__":
    target_ip = "192.168.0.254" # Dummy Target in local subnet
    port_scan(target_ip)
