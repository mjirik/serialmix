from flask import Flask, jsonify, request, send_from_directory
import serial
from pathlib import Path

app = Flask(__name__)

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#

serial_port_0 = "/dev/ttyUSB0"
serial_port_1 = "/dev/ttyUSB1"
baudrate = 19200
baudrate = 9600

debug = True

#TODO prepare the structure of sliders - device, block id, ...
sliders = {
    i:{
        "channel": i,
        "value": 0,
        "mute1": True,
        "mute2": True,
    } for i in range(1,7)
}
connected = False


def serial_set_slider(channel:int, value:int):
    device = 1
    block_id = 207
    send_message(f"SET {device} FDRLVL {block_id} {channel} {value}", port=serial_port_0)

def serial_set_mute(channel:int, value:bool, room_id:int):
    device = 2
    block_id = 207 if room_id == 0 else 208
    send_message(f"SET {device} FDRMUTE {block_id} {channel} {int(value)}", port=serial_port_1)


def init_state():
    """
    Called on device startup. Set all the faders to initial value and mute all.
    :return:
    """
    # initial_value = 0
    # for i in range(0, len(sliders)):
    #     sliders[i]["value"] = initial_value
    #     sliders[i]["mute1"] = True
    #     sliders[i]["mute2"] = True

    send_state()

def send_state():
    for i in range(1, len(sliders) + 1):
        serial_set_slider(channel=i, value=sliders[i]["value"])
        serial_set_mute(channel=i, value=sliders[i]["mute1"], room_id=1)
        serial_set_mute(channel=i, value=sliders[i]["mute2"], room_id=2)


@app.route('/set_serial_device')
def set_serial_port():
    """
    Set port of device 0 or 1
    :return:
    """
    if request.method == "POST":
        id = request.args.get("id")
        port = request.args.get("port")
        if id == 0:
            serial_port_0 = port
        else:
            serial_port_1 = port



@app.route('/set_slider', methods=['POST'])
@cross_origin()
def rest_set_slider():
        print("send_message recieved")
        print(request.json)
        channel = request.json['channel']
        sliders[channel]["value"] = int(request.json['value'])
        serial_set_slider(channel=channel, value=sliders[channel])

        data = {
            # 'id': id,
            "error": False,
        }

        # if not debug:
        response = jsonify(data)
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/set_mute', methods=['POST'])
@cross_origin()
def rest_set_mute():
    print("send_message recieved")
    print(request.json)
    channel = request.json['channel']

    sliders[channel]["value"] = bool(request.json['value'])
    room_id = int(request.json["room_id"])
    mute_key = "mute" + str(room_id)
    sliders[channel][mute_key] = request.json["value"]
    serial_set_mute(channel=channel, value=sliders[channel][mute_key], room_id=room_id)

    data = {
        # 'id': id,
        "error": False,
    }

    # if not debug:
    response = jsonify(data)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_state', methods=['POST'])
@cross_origin()
def get_state():
    response = jsonify(sliders)
    return response

def send_message(message, port):
    port = serial_port_0 if id == 0 else serial_port_1
    # možná globálně
    if not debug:
        with serial.Serial(port, baudrate, timeout=1) as ser:
            ser.write(message.encode("utf-8"))
            ser.flush()
    else:
        print(message)


@app.route('/')
def send_index():
    return send_from_directory(Path(__file__).parent, "index.html")

@app.route('/<path:path>')
def send_dir(path):
    print(f"recived path request {path}")
    return send_from_directory(Path(__file__).parent, path)


if __name__ == "__main__":
    init_state()
    app.run(debug=True, host="0.0.0.0", port=5000)

