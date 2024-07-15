from kafka import KafkaConsumer
from hdfs import InsecureClient
from flask import Flask, jsonify
from flask_cors import CORS
import json
import threading

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'air_quality_data',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

# Initialize HDFS client
hdfs_client = InsecureClient('http://localhost:9870', user='hadoopuser')

# HDFS directory and file path
hdfs_path = '/user/hadoopuser/air_quality_data.json'

# Flask app to serve data
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

data_list = []

# Consume data in a separate thread
def consume_data():
    for message in consumer:
        data = message.value
        data_list.append(data)
        #if len(data_list) > 100:
           #data_list.pop(0)  # Keep only the last 100 data points

        # Write data to HDFS
        with hdfs_client.write(hdfs_path, encoding='utf-8', append=True) as writer:
            writer.write(json.dumps(data) + "\n")

thread = threading.Thread(target=consume_data)
thread.start()

@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_list)

if __name__ == '__main__':
    app.run(debug=True)

