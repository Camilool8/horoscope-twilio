#!/usr/bin/env python3
"""
Simple health check endpoint for the horoscope application
"""
from flask import Flask, jsonify
import threading
import time
import os

app = Flask(__name__)

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'horoscope-sender',
        'timestamp': time.time()
    })

@app.route('/ready')
def readiness_check():
    """Readiness check endpoint"""
    return jsonify({
        'status': 'ready',
        'service': 'horoscope-sender'
    })

def start_health_server():
    """Start the health check server in a separate thread"""
    port = int(os.getenv('HEALTH_PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

if __name__ == '__main__':
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    while True:
        time.sleep(60)