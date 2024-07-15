# producer.py
from kafka import KafkaProducer
import json
import time
import random

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Define the topic
topic = 'air_quality_data'

# Generate and send data
while True:
    data = {
        'timestamp': time.time(),
        'aqi': random.randint(0, 500)  # Simulate AQI values
    }
    producer.send(topic, data)
    print(f"Sent: {data}")
    time.sleep(1)  # Send data every second
