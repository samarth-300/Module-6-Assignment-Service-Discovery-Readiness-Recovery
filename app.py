from flask import Flask, jsonify
import os

app = Flask(__name__)
ready = True

@app.route('/')
def inventory():
    if not ready:
        return jsonify({"error": "Pod is not ready"}), 503
    return jsonify({
        "service": "inventory",
        "pod": os.environ.get("HOSTNAME", "unknown"),
        "message": "Inventory service is running"
    })

@app.route('/health/ready')
def readiness():
    if ready:
        return "ready", 200
    return "not ready", 503

@app.route('/fail-ready', methods=['POST', 'GET'])
def fail_ready():
    global ready
    ready = False
    return "readiness disabled", 200

@app.route('/restore-ready', methods=['POST', 'GET'])
def restore_ready():
    global ready
    ready = True
    return "readiness restored", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
