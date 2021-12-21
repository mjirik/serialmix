from flask import Flask, jsonify, request
import serial

app = Flask(__name__)

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#
incomes = [
  { 'description': 'salary', 'amount': 5000 }
]
serial_port_0 = "/dev/ttyUSB0"
serial_port_1 = "/dev/ttyUSB1"
baudrate = 19200
baudrate = 9600


@app.route('/incomes')
def get_incomes():
    return jsonify(incomes)


@app.route('/incomes', methods=['POST'])
def add_income():
    incomes.append(request.get_json())
    return '', 204

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



@app.route('/send_message', methods=['POST'])
@cross_origin()
def send_message():
        debug = True
        print("send_message recieved")
        # if request.method == "POST":
        # filename = request.args.get("message")
        # exists = Path(filename).exists()
        # id = request.args.get("id")
        # message = request.args.get("message")
        id = 0
        message = "green\n"
        print(request.args)
        print(request.json)
        data = {
            'id': id,
        }

        if not debug:
            port = serial_port_0 if id == 0 else serial_port_1
            # možná globálně
            with serial.Serial(port, 19200, timeout=1) as ser:
                ser.write(message.encode("utf-8"))
                ser.flush()
        response = jsonify(data)
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return response


app.run(debug=True, host="0.0.0.0", port=5000)

