const express = require('express');
const cors = require('cors');
const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'candlestick-consumer',
  brokers: ['localhost:9092'] // Replace with your Kafka broker addresses
});

const consumer = kafka.consumer({ groupId: 'candlestick-group' });
const app = express();
const port = 3000;

app.use(cors()); // Enable CORS

let candlestickData = [];

async function consumeCandlestickData() {
  await consumer.connect();
  await consumer.subscribe({ topic: 'candlestick-data', fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const data = JSON.parse(message.value.toString());
      candlestickData.push(data);
      if (candlestickData.length > 100) { // Keep only the last 100 entries
        candlestickData.shift();
      }
      console.log('Received data:', data);
    },
  });
}

consumeCandlestickData().catch(console.error);

app.get('/data', (req, res) => {
  res.json(candlestickData);
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
