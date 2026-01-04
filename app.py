from flask import Flask, jsonify, send_file
import json
import subprocess
import os

app = Flask(__name__)

# ================= PATH CONFIG =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "log.json")

honeypot_process = None

# ================= ROUTES =================
@app.route("/")
def home():
    return send_file(os.path.join(BASE_DIR, "index.html"))

@app.route("/style.css")
def css():
    return send_file(os.path.join(BASE_DIR, "style.css"))

@app.route("/script.js")
def js():
    return send_file(os.path.join(BASE_DIR, "script.js"))

@app.route("/api/logs")
def get_logs():
    if not os.path.exists(LOG_FILE):
        return jsonify([])

    with open(LOG_FILE, "r") as f:
        return jsonify(json.load(f))

@app.route("/api/start-honeypot")
def start_honeypot():
    global honeypot_process

    if honeypot_process is None:
        honeypot_process = subprocess.Popen(
            ["python", "honeypot.py"],
            cwd=BASE_DIR
        )
        return jsonify({"status": "honeypot started"})

    return jsonify({"status": "honeypot already running"})

@app.route("/api/stop-honeypot")
def stop_honeypot():
    global honeypot_process

    if honeypot_process:
        honeypot_process.terminate()
        honeypot_process = None
        return jsonify({"status": "honeypot stopped"})

    return jsonify({"status": "honeypot not running"})

@app.route("/api/simulate-attack")
def simulate_attack():
    subprocess.Popen(
        ["python", "att.py"],
        cwd=BASE_DIR
    )
    return jsonify({"status": "attack simulation triggered"})

# ================= ENTRY =================
if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port)
