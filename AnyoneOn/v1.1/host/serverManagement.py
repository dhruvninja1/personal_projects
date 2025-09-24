from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
from flask_cors import CORS
import json
import sys
import threading
from datetime import datetime
import requests
import subprocess
import random
import threading


def start_server(port):
        subprocess.run(f"python3 statusServer.py {port}", capture_output=True, text=True, shell=True)

app = Flask(__name__)
CORS(app)

open_servers = []

with open("data/openServers.json", 'r') as file:
        open_servers = json.load(file)


@app.route("/createServer", methods=['GET'])
def createServer():
        result = 0
        while result == 0:
                test_port = random.randint(49152, 65535)
                result = subprocess.run(f"netstat -an | grep LISTEN | grep .{test_port}", capture_output=True, text=True, shell=True)
        open_servers.append(test_port)
        with open("data/openServers.json", 'w') as file:
                json.dump(open_servers, file)
        thread = threading.Thread(target=start_server, args=(test_port,))
        thread.start()
        return(test_port), 

@app.route("/joinServer/<int:port>", methods=['GET'])
def join_server(port):
        if port in open_servers:
                return("Success"), 200
        else:
                return("Not found"), 200
        
@app.route("/deleteServer/<int:port>")
def delete_server(port):
        if port in open_servers:
                subprocess.run(f"kill $(lsof -i:{port})", capture_output=True, text=True, shell=True)
                open_servers.remove(port)
                with open("data/openServers.json", 'w') as file:
                        json.dump(open_servers, file)
                return("Success"), 200
        else:
                return("Server not found"), 200
if __name__ == "__main__":
    app.run(debug=True, port=15565, use_reloader=False)
