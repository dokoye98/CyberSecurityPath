import socket
import os
from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
LOG_DIR = os.path.join(BASE_DIR, "logs")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE = os.path.join(LOG_DIR, "ssh.log")

def log_ssh_attempt(client_ip, username, password):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[ {timestamp} ] - [ {client_ip} ] - Username:{username} - Password:{password}"
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")
    print(f"🚨 Attack detected! {log_entry}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", 22))
server_socket.listen(5)

print("[!] SSH Honeypot Running on Port 22...")

while True:
    try:
        client_socket, client_address = server_socket.accept()
        client_ip  = client_address[0]
        print(f"🔍 Connection from {client_ip}")

        client_socket.sendall(b"Username: ")
        username = client_socket.recv(1024).strip().decode()

        client_socket.sendall(b"Password: ")
        password = client_socket.recv(1024).strip().decode()

        log_ssh_attempt(client_ip, username, password)

        client_socket.sendall(b"Access denied.\n")
        client_socket.close()
    except KeyboardInterrupt:
        print("\n[!] Closing SSH Honeypot...")
        server_socket.close()
        break
    except Exception as e:
        print(f"[!] Error: {e}")
