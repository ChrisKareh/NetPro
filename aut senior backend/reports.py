from flask import Flask, render_template, jsonify
from flask_cors import CORS, cross_origin
import psutil
import time
import os
import pandas as pd
import socket
import platform
import datetime
import uuid

app = Flask(__name__)
CORS(app)

UPDATE_DELAY = 1


def get_size(bytes):
    """
    Returns size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024


def get_system_info():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    mac_address = ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 48, 8)])
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    system_info = {
        'hostname': hostname,
        'ip_address': ip_address,
        'mac_address': mac_address,
        'platform': platform.platform(),
        'system': platform.system(),
        'processor': platform.processor(),
        'architecture': platform.machine(),
        'current_time': current_time
    }
    return system_info


@app.route('/reports')
@cross_origin()
def get_network_stats():
    io = psutil.net_io_counters(pernic=True)

    while True:
        time.sleep(UPDATE_DELAY)

        io_2 = psutil.net_io_counters(pernic=True)

        data = []
        for iface, iface_io in io.items():
            upload_speed = io_2[iface].bytes_sent - iface_io.bytes_sent
            download_speed = io_2[iface].bytes_recv - iface_io.bytes_recv
            data.append({
                "iface": iface,
                "Download": get_size(io_2[iface].bytes_recv),
                "Upload": get_size(io_2[iface].bytes_sent),
                "Upload Speed": f"{get_size(upload_speed / UPDATE_DELAY)}/s",
                "Download Speed": f"{get_size(download_speed / UPDATE_DELAY)}/s",
            })

        io = io_2

        df = pd.DataFrame(data)

        df.sort_values("Download", inplace=True, ascending=False)

        os.system("cls") if "nt" in os.name else os.system("clear")

        return df.to_json(orient='records')


@app.route('/system_info', methods=['GET'])
def system_info():
    info = get_system_info()
    return jsonify(info)


if __name__ == '__main__':
    app.run(port=5003)
