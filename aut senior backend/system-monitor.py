from flask import Flask, jsonify
from flask_cors import CORS,cross_origin
import psutil
import speedtest
import socket
import getmac


app = Flask(__name__)
CORS(app)

@app.route('/api/system-stats')
@cross_origin()
def get_system_stats():
    cpu_usage, memory_usage, disk_usage = _fetch_system_stats()
    return jsonify({
        'cpuUsage': cpu_usage,
        'memoryUsage': memory_usage,
        'diskUsage': disk_usage
    })

@app.route('/api/internet-stats')
def get_internet_stats():
    download_speed, upload_speed = _fetch_internet_stats()
    return jsonify({
        'downloadSpeed': download_speed,
        'uploadSpeed': upload_speed
    })

@app.route('/api/network-info')
def get_network_info():
    ip_address, mac_address = _fetch_network_info()
    return jsonify({
        'ipAddress': ip_address,
        'macAddress': mac_address
    })

def _fetch_system_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return cpu_usage, memory_usage, disk_usage

def _fetch_internet_stats():
    st = speedtest.Speedtest()
    download_speed = st.download() / 10**6  
    upload_speed = st.upload() / 10**6  
    return download_speed, upload_speed

def _fetch_network_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    mac_address = getmac.get_mac_address()
    return ip_address, mac_address

if __name__ == '__main__':
    app.run(port= 5001)
