from flask import Flask, request, jsonify
import math
from datetime import datetime

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_data():
    data = request.json
    vehicle_count = data.get('vehicle_count', 0)
    emergency = data.get('emergency', False)

    if emergency:
        green_signal_time = 40
    else:
        if vehicle_count <= 2:
            green_signal_time = 10
        elif vehicle_count <= 5:
            green_signal_time = 20
        else:
            green_signal_time = 30

    return jsonify({
        'green_signal_time': green_signal_time,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
