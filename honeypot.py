import socket
import json
import os
from datetime import datetime
import pytz

# ================= TIMEZONE =================
IST = pytz.timezone("Asia/Kolkata")

# ================= CONFIG =================
HOST = "0.0.0.0"
PORT = 2222

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "log.json")

# ================= LOGGING =================
def load_logs():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)
        return []

    with open(LOG_FILE, "r") as f:
        return json.load(f)

def write_log(entry):
    logs = load_logs()
    logs.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

def calculate_severity(logs, ip):
    attempts = sum(1 for log in logs if log["source_ip"] == ip)

    if attempts >= 10:
        return "HIGH"
    elif attempts >= 5:
        return "MEDIUM"
    else:
        return "LOW"

# ================= HONEYPOT =================
def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[+] SSH Honeypot listening on {HOST}:{PORT}")
    print(f"[+] Logging to: {LOG_FILE}")

    try:
        while True:
            client, addr = server.accept()
            source_ip, source_port = addr

            logs = load_logs()
            severity = calculate_severity(logs, source_ip)

            print(f"[!] SSH attempt from {source_ip}:{source_port} | Severity: {severity}")

            try:
                client.sendall(b"SSH-2.0-OpenSSH_8.2p1 Ubuntu-4\r\n")
            except:
                pass

            event = {
                "timestamp": datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S"),
                "source_ip": source_ip,
                "source_port": source_port,
                "destination_port": PORT,
                "service": "SSH",
                "event": "connection_attempt",
                "severity": severity,
                "source": "honeypot"
            }

            write_log(event)
            client.close()

    except KeyboardInterrupt:
        print("\n[!] Honeypot stopped by user")
    finally:
        server.close()

# ================= ENTRY =================
if __name__ == "__main__":
    start_honeypot()
