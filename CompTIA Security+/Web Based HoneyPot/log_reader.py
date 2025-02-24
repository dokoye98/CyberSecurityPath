import time

def read_logs():
    try:
        with open("honeypot_log.txt", "r") as log:
            logs = log.readlines()
            if logs:
                print("\n=== Unauthorized Access Attempts ===")
                for line in logs:
                    print(line.strip())
            else:
                print("[*] No unauthorized access attempts logged yet.")
    except FileNotFoundError:
        print("[!] Log file not found.")

if __name__ == "__main__":
    print("[*] Monitoring Honeypot Logs...")
    while True:
        read_logs()
        time.sleep(5)