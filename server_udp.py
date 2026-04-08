import socket
import json
import threading
import time
from collections import defaultdict
from encryption import decrypt

HOST = '0.0.0.0'
PORT = 12345

event_counts = defaultdict(lambda: defaultdict(int))
lock = threading.Lock()

def process_packet(data: bytes, addr: tuple):
    try:
        decrypted = decrypt(data)
        message = json.loads(decrypted.decode('utf-8'))

        node_id = message['node_id']
        event_type = message['event_type']

        with lock:
            event_counts[node_id][event_type] += 1

        print(f"[{time.strftime('%H:%M:%S')}] Received from Node {node_id} ({addr[0]}:{addr[1]}): {event_type}")
    except Exception as e:
        print(f"❌ Error processing packet from {addr}: {e}")

def display_aggregates():
    while True:
        time.sleep(5)
        with lock:
            if not event_counts:
                continue
            print("\n" + "="*70)
            print("📊 AGGREGATED EVENT VISUALIZATION (Edge-filtered)")
            print("="*70)
            for node, counts in sorted(event_counts.items()):
                print(f"Node {node:2d} → {dict(counts)}")
            print("="*70 + "\n")

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   # ← Prevents port-in-use error
    sock.bind((HOST, PORT))
    print(f"🔐 UDP Server with AES-256-CBC listening on {HOST}:{PORT}")

    # Background thread for visualization
    threading.Thread(target=display_aggregates, daemon=True).start()

    print("✅ Ready to handle multiple concurrent clients...")

    while True:
        data, addr = sock.recvfrom(4096)
        # Process each client in its own thread (true concurrency)
        threading.Thread(target=process_packet, args=(data, addr), daemon=True).start()