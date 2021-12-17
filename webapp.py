from flask import Flask, jsonify, request

app = Flask(__name__)

#
incomes = [
  { 'description': 'salary', 'amount': 5000 }
]
serial_port_0 = "/dev/ttyUSB0"
serial_port_1 = "/dev/ttyUSB1"


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



@app.route('/send_message')
def send_message():
        print("send_message recieved")
    # if request.method == "POST":
        # filename = request.args.get("message")
        # exists = Path(filename).exists()
        # id = request.args.get("id")
        # message = request.args.get("message")
        id = 0
        message = "green\n"

        port = serial_port_0 if id == 0 else serial_port_1
        # možná globálně
        with serial.Serial(port, 19200, timeout=1) as ser:
            ser.write(message.encode("utf-8"))
            ser.flush()
            # x = ser.read()  # read one byte
            # s = ser.read(10)  # read up to ten bytes (timeout)
            # line = ser.readline()  # read a '\n' terminated line


app.run(debug=True, host="0.0.0.0", port=5000)

