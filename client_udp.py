import socket
import json
import time
import random
import sys
from encryption import encrypt

HOST = '127.0.0.1'      # Change to your server IP if running on different machines
PORT = 12345
NODE_ID = int(sys.argv[1]) if len(sys.argv) > 1 else 1

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"🔐 Client Node {NODE_ID} started (UDP + AES-256-CBC)")

    event_types = ['failure', 'threshold', 'info']

    while True:
        event_type = random.choice(event_types)

        # EDGE FILTERING: only send critical events
        if event_type in ['failure', 'threshold']:
            message = {
                "node_id": NODE_ID,
                "event_type": event_type,
                "details": f"Simulated {event_type} on node {NODE_ID}",
                "timestamp": time.time()
            }

            # Simulate packet loss (15%)
            if random.random() < 0.15:
                print(f"Node {NODE_ID} → Packet lost (simulated)")
            else:
                encrypted = encrypt(json.dumps(message).encode('utf-8'))
                sock.sendto(encrypted, (HOST, PORT))
                print(f"Node {NODE_ID} → Sent critical event: {event_type}")
        else:
            print(f"Node {NODE_ID} → Filtered (non-critical): {event_type}")

        time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\nClient Node {NODE_ID} shutting down gracefully.")
    except Exception as e:
        print(f"Client error: {e}")