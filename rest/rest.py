from flask import Flask, jsonify, request, send_from_directory
import serial
from pathlib import Path
import traceback
import time
import sys
import argparse
import inspect

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

debug_no_serial = True
debug_no_serial = False

# TODO Zde se nastavuje počet faderů
number_of_sliders = 6

sliders = {
    i:{
        "channel": i,
        "value": 0,
        "mute1": True,
        "mute2": True,
    } for i in range(1, number_of_sliders + 1)
}

connection_error = False
connetcion_error_message = ""


def serial_set_slider(channel:int, value:int):
    device = 1
    block_id = 259
    send_message(f"SET {device} FDRLVL {block_id} {channel} {value}\n", port=serial_port_0)

def serial_set_mute(channel:int, value:bool, room_id:int):
    device = 2
    block_id = 276 if room_id == 1 else 275
    send_message(f"SET {device} MBMUTE {block_id} {channel} {int(value)}\n", port=serial_port_0)

def serial_projector(id:str):
    """
    Messages from other buttons on the page with class button-projector
    :param id:
    :return:
    """

    #TODO nastavit zprávy pro seriovou linku v projektoru
    if id == "p1":
        # device = 1
        send_message(f"PROJECTOR POWER ON\n", port=serial_port_0)
    elif id == "p2":
        send_message(f"PROJECTOR POWER OFF\n", port=serial_port_0)
    elif id == "p3":
        send_message(f"PROJECTOR SOURCE HDMI\n", port=serial_port_0)
    elif id == "p4":
        send_message(f"PROJECTOR SOURCE VGA\n", port=serial_port_0)

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
    print(inspect.stack())
    print(send_message("GET 0 IPADDR\n", port=serial_port_0, wait_for_response=True))
    # print(send_message("GET 0 IPADDR\n", port=serial_port_1, wait_for_response=True))
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
    printt(f"send_message recieved json={request.json}")
    # printt(request.json)
    channel = request.json['channel']
    sliders[channel]["value"] = int(request.json['value'])
    serial_set_slider(channel=channel, value=sliders[channel]['value'])

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

@app.route('/projector', methods=['POST'])
@cross_origin()
def rest_projector():
    printt(f"projector json={request.json}")
    # printt(request.json)
    id = request.json['id']
    # sliders[channel]["value"] = int(request.json['value'])
    serial_projector(id)
    # serial_set_slider(channel=channel, value=sliders[channel]['value'])

    data = {
        "error": connection_error,
        "message": connetcion_error_message,
    }
    response = jsonify(data)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response


def send_message(message:str, port:str, wait_for_response=False):
    global connetcion_error_message
    global connection_error
    # port = serial_port_0 if port == 0 else serial_port_1
    # možná globálně
    recived_message = ''

    if not debug_no_serial:

        try:
            with serial.Serial(port, baudrate, timeout=1, parity=parity, stopbits=stopbits) as ser:
                printt(f"port={port} sended_message={message.encode('ascii')}")
                ser.write(message.encode("ascii"))
                ser.flush()
                if wait_for_response:
                    recived_message = ser.read(100)
                    printt(f"port={port} recived_message={recived_message}")
        except Exception as e:
            traceback.print_exc()
            connection_error = True
            connetcion_error_message = traceback.format_exc() + f"\n\nport{port}"

    else:
        printt(f"port={port} sended_message={message.encode('ascii')}")

    return recived_message


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Serial Mix REST API')
    parser.add_argument('--debug-no-serial', action='store_true',
                    help='Print the serial messages instead of sending it to the serial port')
    args = parser.parse_args()
    print("Serial Mix REST Api starting...")
    if args.debug_no_serial:
        debug_no_serial = True
    time.sleep(start_sleep_time_seconds)
    init_state()
    app.run(
        debug=False,
        # debug=True,
        # use_reloader=False,
        host="0.0.0.0",
        port=5000
    )

