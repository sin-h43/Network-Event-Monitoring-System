import socket
import threading
from cryptography.fernet import Fernet

PORT = 8888

# Shared secret key (must be same on client)
key = b'6L1YHh7fXK1gTtNqY8hK4s5Y0Fh2mP7Q9p3wE6R8tU0='
cipher = Fernet(key)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("0.0.0.0", PORT))

print(f"🔒 Secure UDP Server running on port {PORT}")
print("Waiting for clients...\n")

clients = set()

def listen():
    while True:
        try:
            data, addr = server.recvfrom(4096)

            if addr not in clients:
                clients.add(addr)
                print(f"✅ New client joined: {addr}")

            # decrypt message
            message = cipher.decrypt(data).decode()

            print(f"📨 {addr}: {message}")

            # broadcast encrypted message
            for client in clients:
                if client != addr:
                    encrypted = cipher.encrypt(f"{addr}: {message}".encode())
                    server.sendto(encrypted, client)

        except Exception as e:
            print("Error:", e)

threading.Thread(target=listen, daemon=True).start()

while True:
    msg = input("Server message: ")

    encrypted = cipher.encrypt(f"Server: {msg}".encode())

    for client in clients:
        server.sendto(encrypted, client)