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
            if received_data["till_hr"] != '':
                tillHr = int(received_data["till_hr"])
                tillMin = int(received_data["till_min"])
                if ((tillHr <= 23 and tillHr >= 0) and (tillMin <= 59 or tillMin == '')):
                    item["till_hr"] = tillHr
                    if tillMin == '':
                        item["till_min"] = 0
                    else:
                        item["till_min"] = tillMin
                else:
                    item["till_min"] = ''
                    item["till_hr"] = ''
            else:
                item["till_min"] = ''
                item["till_hr"] = ''

            found=True
            break

    if not found:
        if received_data["till_hr"] != '':
                tillHr = int(received_data["till_hr"])
                tillMin = int(received_data["till_min"])
                if ((tillHr <= 23 and tillHr >= 0) and (tillMin <= 59 or tillMin == '')):
                    if tillMin == '':
                        item["till_min"] = 0
                else:
                    item["till_min"] = ''
                    item["till_hr"] = ''
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
