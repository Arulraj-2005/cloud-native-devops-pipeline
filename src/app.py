from flask import Flask, jsonify, render_template
import psutil
import os
from datetime import datetime

app = Flask(__name__)

DEPLOY_TIME = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

def get_metrics():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "cpu_percent": cpu,
        "memory_total_gb": round(mem.total / (1024 ** 3), 2),
        "memory_used_gb": round(mem.used / (1024 ** 3), 2),
        "memory_percent": mem.percent,
        "disk_total_gb": round(disk.total / (1024 ** 3), 2),
        "disk_used_gb": round(disk.used / (1024 ** 3), 2),
        "disk_percent": disk.percent,
        "deploy_time": DEPLOY_TIME,
        "pod_name": os.environ.get("POD_NAME", "local"),
        "pod_namespace": os.environ.get("POD_NAMESPACE", "default"),
        "node_name": os.environ.get("NODE_NAME", "localhost"),
        "app_version": os.environ.get("APP_VERSION", "1.0.0"),
    }

@app.route("/")
def dashboard():
    metrics = get_metrics()
    return render_template("dashboard.html", **metrics)

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()}), 200

@app.route("/api/metrics")
def api_metrics():
    return jsonify(get_metrics()), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
