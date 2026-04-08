import socket
import os
from encryption import encrypt

HOST = '127.0.0.1'
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Sending error packets to server...")

# 1. Plaintext garbage
sock.sendto(b"PLAINTEXT GARBAGE", (HOST, PORT))

# 2. Random bytes
sock.sendto(os.urandom(64), (HOST, PORT))

# 3. Valid encryption + invalid JSON
sock.sendto(encrypt(b"not json"), (HOST, PORT))

# 4. Missing required field
sock.sendto(encrypt(b'{"node_id": 1}'), (HOST, PORT))

# 5. Tampered packet (corrupt valid encrypted data)
valid = encrypt(b'{"node_id": 1, "event_type": "failure"}')
corrupt = bytearray(valid)
corrupt[20] ^= 0xFF
sock.sendto(bytes(corrupt), (HOST, PORT))

sock.close()
print("Done! Check server terminal for errors.")