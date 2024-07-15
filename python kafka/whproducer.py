# producer.py
from kafka import KafkaProducer
import json
import time
import requests

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# OpenWeatherAPI settings
api_key = '76e674b757128f72511ad39683ec45b1'
location = 'Delhi'
url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}'

# Define the topic
topic = 'weather_data'

# Fetch and send data
while True:
    response = requests.get(url)
    data = response.json()
    producer.send(topic, data)
    print(f"Sent: {data}")
    time.sleep(60)  # Fetch data every minute
