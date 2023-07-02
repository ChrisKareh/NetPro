from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import psutil
from collections import defaultdict
from datetime import datetime
import time
from scapy.all import ifaces, sniff
from threading import Thread

app = Flask(__name__)
CORS(app)


all_macs = {iface.mac for iface in ifaces.values()}

connection2pid = {}

pid2traffic = defaultdict(lambda: [0, 0])

is_program_running = True


def get_size(bytes):
    """
    Returns the size of bytes in a nice format
    """
    for unit in ['', 'K', 'M', 'G', 'T', 'P']:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}B"
        bytes /= 1024


def process_packet(packet):
    global pid2traffic
    try:
        
        packet_connection = (packet.sport, packet.dport)
    except (AttributeError, IndexError):
        
        pass
    else:
        
        packet_pid = connection2pid.get(packet_connection)
        if packet_pid:
            if packet.src in all_macs:
                
                pid2traffic[packet_pid][0] += len(packet)
            else:
                
                pid2traffic[packet_pid][1] += len(packet)


def get_connections():
    """A function that keeps listening for connections on this machine
    and adds them to the `connection2pid` global variable"""
    global connection2pid
    while is_program_running:
    
        for c in psutil.net_connections():
            if c.laddr and c.raddr and c.pid:
               
                connection2pid[(c.laddr.port, c.raddr.port)] = c.pid
                connection2pid[(c.raddr.port, c.laddr.port)] = c.pid
      
        time.sleep(1)


def calculate_stats():
    global pid2traffic
    processes = {}
    for pid, traffic in pid2traffic.items():
        try:
            p = psutil.Process(pid)
            name = p.name()
            create_time = datetime.fromtimestamp(p.create_time())
            upload = traffic[0]
            download = traffic[1]
            upload_speed = traffic[0]
            download_speed = traffic[1]
            process = {
                "name": name,
                "create_time": create_time,
                "upload": upload,
                "download": download,
                "upload_speed": upload_speed,
                "download_speed": download_speed,
            }
            processes[pid] = process
        except (psutil.NoSuchProcess, KeyError):
            pass
    return processes


def get_stats():
    global pid2traffic
    stats = calculate_stats()
    stats = {pid: {
        "name": process["name"],
        "create_time": process["create_time"].strftime("%Y-%m-%d %H:%M:%S"),
        "upload": get_size(process["upload"]),
        "download": get_size(process["download"]),
        "upload_speed": get_size(process["upload_speed"]),
        "download_speed": get_size(process["download_speed"])
    } for pid, process in stats.items()}
    return stats


@app.route('/analytics')
@cross_origin()
def network_stats():
    return jsonify(get_stats())


if __name__ == "__main__":
    connections_thread = Thread(target=get_connections)
    connections_thread.start()
    sniff_thread = Thread(target=sniff, kwargs={"prn": process_packet, "store": False})
    sniff_thread.start()
    app.run(port=5002)

