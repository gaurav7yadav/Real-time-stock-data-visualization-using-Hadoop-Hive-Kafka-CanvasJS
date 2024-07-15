const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'chart-producer',
  brokers: ['localhost:9092']
});

const producer = kafka.producer();

const run = async () => {
  await producer.connect();
  let x = 1;

  setInterval(async () => {
    const y = Math.floor(Math.random() * 100);
    const message = { x, y };
    await producer.send({
      topic: 'chart-data',
      messages: [{ value: JSON.stringify(message) }],
    });
    console.log('Message sent:', message);
    x++;
  }, 1000);
};

run().catch(console.error);
