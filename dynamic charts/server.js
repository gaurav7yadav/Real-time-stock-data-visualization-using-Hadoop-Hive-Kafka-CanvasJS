const express = require('express');
const { Kafka } = require('kafkajs');
const cors = require('cors');  // Import cors

const app = express();
const port = 3000;

// Enable CORS for all routes
app.use(cors());

const kafka = new Kafka({
  clientId: 'chart-consumer',
  brokers: ['localhost:9092']
});

const consumer = kafka.consumer({ groupId: 'chart-group' });

const messages = [];

const runConsumer = async () => {
  await consumer.connect();
  await consumer.subscribe({ topic: 'chart-data', fromBeginning: true });

  await consumer.run({
    eachMessage: async ({ topic, partition, message }) => {
      const data = JSON.parse(message.value.toString());
      messages.push(data);
      if (messages.length > 10) {
        //messages.shift();
      }
      console.log(`Received message: ${data}`); // Log received messages
    },
  });
};

runConsumer().catch(console.error);

app.get('/data', (req, res) => {
  res.json(messages);
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
