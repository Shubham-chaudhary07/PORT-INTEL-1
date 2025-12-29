import json
import random
import os
from datetime import datetime
import pytz

# ================= TIMEZONE =================
IST = pytz.timezone("Asia/Kolkata")

# ================= PATH CONFIG =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "log.json")

# ================= FAKE ATTACKER IP POOL =================
FAKE_IPS = [
    "45.83.12.91",
    "103.221.234.17",
    "185.220.101.42",
    "91.240.118.172",
    "203.0.113.55",
    "192.168.1.15"
]

# ================= LOG HELPERS =================
def load_logs():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LOG_FILE, "r") as f:
        return json.load(f)

def save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=4)

# ================= SIMULATED ATTACK ENGINE =================
def simulate_attacks(count=30):
    logs = load_logs()

    for _ in range(count):
        event = {
            "timestamp": datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S"),
            "source_ip": random.choice(FAKE_IPS),
            "source_port": random.randint(1, 8000),  # real ephemeral range
            "destination_port": 2222,
            "service": "SSH",
            "event": "connection_attempt",
            "severity": random.choice(["LOW", "MEDIUM", "HIGH"]),
            "source": "simulation"
        }

        logs.append(event)

    save_logs(logs)
    print(f"[+] Simulated {count} SSH attack events (IST time)")

# ================= ENTRY =================
if __name__ == "__main__":
    simulate_attacks()
