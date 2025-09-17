from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import json
import sys

argv = sys.argv
PORT = argv[1]
filename = f"data/{PORT}.json"


app = Flask(__name__)
CORS(app)

data = []

with open(filename, 'r') as file:
    data = json.load(file)


@app.route("/status", methods=['POST'])
def get_status():
    global data
    with open(filename, 'r') as file:
        data = json.load(file)
    received_data = request.get_json()
    found = False
    for item in data:
        if item["name"] == received_data["name"]:
            item["status"] = received_data["status"]
            found=True
            break

    if not found:
        data.append(received_data)
    with open(filename, "w") as json_file:
        json.dump(data, json_file)
    return jsonify({"message": "Status updated successfully!"}), 200

@app.route("/statuses", methods=['GET'])
def send_statuses():
    global data
    with open(filename, 'r') as file:
        data = json.load(file)
    return jsonify(data), 200

if __name__ == "__main__":
    app.run(debug=True, port=PORT)
