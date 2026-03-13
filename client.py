import socket
import threading
from cryptography.fernet import Fernet

SERVER_IP = "127.0.0.1"
PORT = 8888

# same key as server
key = b'6L1YHh7fXK1gTtNqY8hK4s5Y0Fh2mP7Q9p3wE6R8tU0='
cipher = Fernet(key)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("🔒 Secure client connected")
print("Type messages (quit to exit)\n")

def receive():
    while True:
        try:
            data, _ = client.recvfrom(4096)

            message = cipher.decrypt(data).decode()

            print("\n" + message)
            print("> ", end="", flush=True)

        except:
            break

threading.Thread(target=receive, daemon=True).start()

while True:
    msg = input("> ")

    if msg.lower() == "quit":
        break

    encrypted = cipher.encrypt(msg.encode())

    client.sendto(encrypted, (SERVER_IP, PORT))

client.close()
print("Disconnected")