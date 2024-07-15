# consumer.py
from kafka import KafkaConsumer
from flask import Flask, jsonify
from flask_cors import CORS
import json
import threading

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'weather_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Flask app to serve data
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

data_list = []

# Consume data in a separate thread
def consume_data():
    global data_list
    for message in consumer:
        data = message.value
        # Ensure the 'dt' key exists
        if 'dt' in data:
            # Extract the necessary fields for plotting
            data_point = {
                'timestamp': data['dt'],
                'temperature': data['main']['temp'] - 273.15,  # Convert Kelvin to Celsius
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed']
            }
            data_list.append(data_point)
            if len(data_list) > 100:
                data_list.pop(0)  # Keep only the last 100 data points

thread = threading.Thread(target=consume_data)
thread.start()

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(debug=True)
