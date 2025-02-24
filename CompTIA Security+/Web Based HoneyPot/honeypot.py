from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import datetime
from mfa_handler import send_firebase_otp
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SERVER_IP = os.getenv("SERVER_IP", "127.0.0.1")
PORT = int(os.getenv("PORT", "5000"))

failed_Attempts = {}
html_dir = "templates"


def load_users(filename):
    users = {}
    if not os.path.exists(filename):
        print(f"[!] Warning: {filename} not found. Skipping...")
        return users
    with open(filename, "r") as file:
          for line in file:
            parts = line.strip().split(":")
            if len(parts) == 3:
                username, password, phone = parts
            elif len(parts) == 2:
                username, password = parts
                phone = "0000000000"  #False phone number
            else:
                print(f"[!] Invalid entry in {filename}: {line.strip()}")
                continue
            users[username] = {"password": password, "phone": phone}
    return users


Authorized_Users = load_users("approved_users.txt")
Honeypot_Users = load_users("users.txt")


def log_honeypot_attempt(username, password, client_ip):
    log_entry = f"[{datetime.datetime.now()}] IP: {client_ip} | Username: {username} | Password: {password}\n"
    with open("honeypot.txt", "a+") as log:
        log.write(log_entry)
    print("[!] Unauthorized Access Logged:", log_entry.strip())


class HoneypotHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.serve_html("index.html")
        elif self.path == "/otp.html":
            self.serve_html("otp.html")
        elif self.path == "/success.html":
            self.serve_html("success.html")
        elif self.path == "/error.html":
            self.serve_html("error.html")
        else:
            self.send_error(404, "Page Not Found")

    def serve_html(self, filename):
        try:
            filepath = os.path.join(html_dir, filename)
            with open(filepath, "r") as file:
                content = file.read()
                content = content.replace("{{ server_ip }}", SERVER_IP).replace("{{ port }}", str(PORT))
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_error(404, "File Not Found")

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        credentials = urllib.parse.parse_qs(post_data)

        username = credentials.get("username", [""])[0]
        password = credentials.get("password", [""])[0]
        client_ip = self.client_address[0]

        if client_ip not in failed_Attempts:
            failed_Attempts[client_ip] = 0

        if username in Honeypot_Users:
            log_honeypot_attempt(username, password, client_ip)
            self.send_response(302)
            self.send_header("Location", "/error.html")
            self.end_headers()
            return  

        if username in Authorized_Users:
            if password == Authorized_Users[username]["password"]:
                failed_Attempts[client_ip] = 0
                phone_number = Authorized_Users[username]["phone"]
                send_firebase_otp(phone_number)
                self.send_response(302)
                self.send_header("Location", "/otp.html")
                self.end_headers()
            else:
                failed_Attempts[client_ip] += 1
        else:
            log_honeypot_attempt(username, password, client_ip)
            failed_Attempts[client_ip] = 3  

        if failed_Attempts[client_ip] >= 3:
            failed_Attempts[client_ip] = 0
            self.send_response(302)
            self.send_header("Location", "/error.html")
            self.end_headers()
        else:
            self.send_response(401)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h2>Login Failed</h2><p>Invalid credentials. Please try again.</p></body></html>")


def run(server_class=HTTPServer, handler_class=HoneypotHandler, port=PORT):
    server_address = ("0.0.0.0", port)
    httpd = server_class(server_address, handler_class)
    print(f"[*] Honeypot running on Hidden IP:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
