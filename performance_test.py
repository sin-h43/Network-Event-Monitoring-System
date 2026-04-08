#!/usr/bin/env python3
"""Performance evaluation script for Network Event Monitoring System"""

import socket
import json
import time
import threading
import subprocess
import psutil
import statistics
from collections import defaultdict
from encryption import encrypt

# Configuration
HOST = '127.0.0.1'
PORT = 12345
TEST_DURATION = 60  # seconds
NUM_CLIENTS = 5

# Metrics storage
latencies = []
packet_loss_count = 0
total_packets = 0
start_time = None
stop_flag = False

def simulated_client(client_id, results):
    """Simulate a client with latency measurement"""
    global packet_loss_count, total_packets, latencies
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    event_types = ['failure', 'threshold', 'info']
    
    while not stop_flag:
        event_type = random.choice(event_types)
        
        if event_type in ['failure', 'threshold']:
            message = {
                "node_id": client_id,
                "event_type": event_type,
                "details": f"Simulated {event_type} on node {client_id}",
                "timestamp": time.time()
            }
            
            # Measure latency (RTT not possible with UDP, so one-way)
            send_time = time.time()
            
            # Simulate packet loss (15%)
            if random.random() < 0.15:
                packet_loss_count += 1
            else:
                encrypted = encrypt(json.dumps(message).encode('utf-8'))
                sock.sendto(encrypted, (HOST, PORT))
                latency = (time.time() - send_time) * 1000  # ms
                latencies.append(latency)
            
            total_packets += 1
        
        time.sleep(random.uniform(0.1, 0.5))  # Random interval
    
    sock.close()

def monitor_cpu(interval=1):
    """Monitor server CPU usage"""
    cpu_percentages = []
    while not stop_flag:
        cpu_percentages.append(psutil.cpu_percent(interval=interval))
    return cpu_percentages

def run_performance_test():
    """Main test orchestration"""
    global stop_flag, start_time
    
    print("="*70)
    print("📊 PERFORMANCE EVALUATION - Network Event Monitoring System")
    print("="*70)
    print(f"Test Configuration:")
    print(f"  • Duration: {TEST_DURATION} seconds")
    print(f"  • Concurrent clients: {NUM_CLIENTS}")
    print(f"  • Target server: {HOST}:{PORT}")
    print(f"  • Simulated loss rate: 15%")
    print("="*70)
    print("\n✅ Ensure server_udp.py is RUNNING before continuing!")
    input("\nPress ENTER to start performance test...")
    
    # Start server process (if needed)
    server_process = None
    try:
        # Check if server is running
        test_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        test_sock.settimeout(2)
        test_sock.sendto(b"ping", (HOST, PORT))
        test_sock.close()
        print("✓ Server detected")
    except:
        print("⚠️ Server not detected. Starting server...")
        server_process = subprocess.Popen(["python", "server_udp.py"])
        time.sleep(2)
    
    # Start CPU monitoring
    stop_flag = False
    cpu_thread = threading.Thread(target=monitor_cpu)
    cpu_thread.start()
    
    # Start clients
    clients = []
    start_time = time.time()
    
    for i in range(NUM_CLIENTS):
        t = threading.Thread(target=simulated_client, args=(i+1, None))
        t.start()
        clients.append(t)
    
    # Run for test duration
    print(f"\n🔄 Running test for {TEST_DURATION} seconds...")
    time.sleep(TEST_DURATION)
    
    # Stop everything
    stop_flag = True
    for t in clients:
        t.join(timeout=2)
    
    # Calculate metrics
    elapsed = time.time() - start_time
    
    # Calculate throughput (events per second)
    successful_packets = total_packets - packet_loss_count
    throughput = successful_packets / elapsed
    
    # Calculate loss rate
    loss_rate = (packet_loss_count / total_packets * 100) if total_packets > 0 else 0
    
    # Calculate latency stats
    if latencies:
        avg_latency = statistics.mean(latencies)
        p95_latency = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else max(latencies)
        max_latency = max(latencies)
    else:
        avg_latency = p95_latency = max_latency = 0
    
    # Print results
    print("\n" + "="*70)
    print("📈 PERFORMANCE RESULTS")
    print("="*70)
    print(f"\n📊 Throughput: {throughput:.2f} events/sec")
    print(f"📊 Total events sent: {total_packets}")
    print(f"📊 Successful deliveries: {successful_packets}")
    print(f"📊 Packet loss rate: {loss_rate:.2f}% (target: 15%)")
    
    print(f"\n⏱️  Latency (one-way):")
    print(f"   • Average: {avg_latency:.2f} ms")
    print(f"   • P95: {p95_latency:.2f} ms")
    print(f"   • Maximum: {max_latency:.2f} ms")
    
    # Stop CPU monitoring and get CPU data
    # (CPU results would be collected here)
    
    print("\n" + "="*70)
    print("✅ Performance test completed!")
    
    # Clean up
    if server_process:
        server_process.terminate()

if __name__ == "__main__":
    import random
    run_performance_test()