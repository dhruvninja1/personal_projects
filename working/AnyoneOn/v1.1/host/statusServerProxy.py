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


app = Flask(__name__)
CORS(app)

open_servers = []
with open("data/openServers.json", 'r') as file:
        open_servers = json.load(file)


@app.route('/<int:port_number>/<path:rest_of_path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(port_number, rest_of_path):
    with open("data/openServers.json", 'r') as file:
        open_servers = json.load(file)
    if port_number in open_servers:
        target_url = f"http://localhost:{port_number}/{rest_of_path}"
        response = requests.request(
            method=request.method,
            url=target_url,
            headers={key: value for (key, value) in request.headers},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [
            (name, value) for (name, value) in response.raw.headers.items()
            if name.lower() not in excluded_headers
        ]

        return Response(response.content, response.status_code, headers)
    else:
        return "Sever not found", 404


app.run(debug=True, port=15555, use_reloader=False)
