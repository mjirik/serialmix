from flask import Flask, jsonify, request, send_from_directory
import serial
from pathlib import Path
import traceback

app = Flask(__name__)

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
#


@app.route('/')
def send_index():
    return send_from_directory(Path(__file__).parent, "index.html")

@app.route('/<path:path>')
def send_dir(path):
    print(f"recived path request {path}")
    return send_from_directory(Path(__file__).parent, path)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)

