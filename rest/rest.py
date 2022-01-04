from flask import Flask, jsonify, request, send_from_directory
import serial
from pathlib import Path
import traceback
import time
import sys

app = Flask(__name__)

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#

serial_port_0 = "/dev/ttyUSB0"
serial_port_1 = "/dev/ttyUSB1"
baudrate = 38400
parity="N"
stopbits = 1

start_sleep_time_seconds = 0

debug = True
debug = False

#TODO prepare the structure of sliders - device, block id, ...
sliders = {
    i:{
        "channel": i,
        "value": 0,
        "mute1": True,
        "mute2": True,
    } for i in range(1,7)
}

connection_error = False
connetcion_error_message = ""


def serial_set_slider(channel:int, value:int):
    device = 1
    block_id = 259
    send_message(f"SET {device} FDRLVL {block_id} {channel} {value}\n", port=serial_port_0)

def serial_set_mute(channel:int, value:bool, room_id:int):
    device = 2
    block_id = 276 if room_id == 0 else 275
    send_message(f"SET {device} FDRMUTE {block_id} {channel} {int(value)}\n", port=serial_port_1)


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

    print("Connection init")
    print(send_message("GET 0 IPADDR\n", port=serial_port_0))
    print(send_message("GET 0 IPADDR\n", port=serial_port_1))
    send_state()

def printt(msg):
    print(msg, file=sys.stderr)

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
    printt("send_message recieved")
    printt(request.json)
    channel = request.json['channel']
    sliders[channel]["value"] = int(request.json['value'])
    serial_set_slider(channel=channel, value=sliders[channel])

    data = {
        "error": connection_error,
        "message": connetcion_error_message,
    }
    response = jsonify(data)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/set_mute', methods=['POST'])
@cross_origin()
def rest_set_mute():
    printt("send_message recieved")
    printt(request.json)
    channel = request.json['channel']

    sliders[channel]["value"] = bool(request.json['value'])
    room_id = int(request.json["room_id"])
    mute_key = "mute" + str(room_id)
    sliders[channel][mute_key] = request.json["value"]
    serial_set_mute(channel=channel, value=sliders[channel][mute_key], room_id=room_id)

    data = {
        # 'id': id,
        "error": connection_error,
        "message": connetcion_error_message,
    }
    # if not debug:
    response = jsonify(data)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get_state', methods=['POST'])
@cross_origin()
def get_state():

    response = jsonify({
        "state": sliders,
        "error": {
            "error": connection_error,
            "message": connetcion_error_message
        }
    })
    return response


def send_message(message:str, port:str):
    global connetcion_error_message
    global connection_error
    # port = serial_port_0 if port == 0 else serial_port_1
    # možná globálně
    recived_message = ''

    if not debug:

        try:
            with serial.Serial(port, baudrate, timeout=1, parity=parity, stopbits=stopbits) as ser:
                printt(f"sended_message={message.encode('ascii')}")
                ser.write(message.encode("ascii"))
                ser.flush()
                recived_message = ser.read(100)
                printt(f"recived_message={recived_message}")
        except Exception as e:
            traceback.print_exc()
            connection_error = True
            connetcion_error_message = traceback.format_exc()

    else:
        print(message)

    return recived_message


if __name__ == "__main__":
    print("Serial Mix REST Api starting...")
    time.sleep(start_sleep_time_seconds)
    init_state()
    app.run(debug=True, host="0.0.0.0", port=5000)

