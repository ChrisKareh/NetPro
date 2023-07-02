from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from ping3 import ping, verbose_ping
import uuid

app = Flask(__name__)
CORS(app)

hosts = {}


@app.route('/add', methods=['POST'])
@cross_origin()
def add_host():
    host = request.form['host']
    ip_address = request.form['ip_address']
    host_id = str(uuid.uuid4())  # Generate a unique ID
    hosts[host_id] = {'host': host, 'ip_address': ip_address}
    return jsonify(
        message=f"Host {host} with IP address {ip_address} and ID {host_id} has been added."
    )


@app.route('/remove/<string:host_id>', methods=['DELETE'])
@cross_origin()
def remove_host(host_id):
    if host_id in hosts:
        host = hosts[host_id]['host']
        del hosts[host_id]
        return jsonify(
            message=f"Host {host} with ID {host_id} has been removed."
        )
    else:
        return jsonify(
            message=f"Host with ID {host_id} not found."
        )


@app.route('/display')
@cross_origin()
def display_hosts():
    if hosts:
        host_list = []
        for host_id, host_data in hosts.items():
            host_list.append({
                "id": host_id,
                "host": host_data['host'],
                "ip_address": host_data['ip_address']
            })
        return jsonify(hosts=host_list)
    else:
        return jsonify(
            message="No hosts found."
        )


@app.route('/check')
@cross_origin()
def check_host_availability():
    if hosts:
        result = []
        for host_id, host_data in hosts.items():
            response_time = ping(host_data['ip_address'])
            if response_time is not None:
                result.append({
                    "id": host_id,
                    "host": host_data['host'],
                    "ip_address": host_data['ip_address'],
                    "availability": True,
                    "response_time": response_time
                })
            else:
                result.append({
                    "id": host_id,
                    "host": host_data['host'],
                    "ip_address": host_data['ip_address'],
                    "availability": False
                })
        return jsonify(hosts=result)
    else:
        return jsonify(
            message="No hosts found."
        )


if __name__ == '__main__':
    app.run(port=5005)
