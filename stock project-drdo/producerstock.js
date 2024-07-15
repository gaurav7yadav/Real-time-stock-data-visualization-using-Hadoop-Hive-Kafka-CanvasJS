const { Kafka } = require('kafkajs');

const kafka = new Kafka({
  clientId: 'candlestick-producer',
  brokers: ['localhost:9092'] // Replace with your Kafka broker addresses
});

const producer = kafka.producer();

async function produceCandlestickData() {
  await producer.connect();
  console.log('Producer connected');

  function getRandomPrice(base) {
    const fluctuation = Math.random() * 10; // random fluctuation within 10 units
    return +(base + fluctuation).toFixed(2);
  }

  function generateCandlestickData(date) {
    const open = getRandomPrice(100);
    const high = getRandomPrice(open + 5);
    const low = getRandomPrice(open - 5);
    const close = getRandomPrice(low + (high - low) / 2);
    
    return {
      date: date.toISOString().split('T')[0],
      open,
      high,
      low,
      close
    };
  }

  let date = new Date(2018, 3, 1);

  setInterval(async () => {
    const data = generateCandlestickData(date);
    date.setDate(date.getDate() + 1);

    await producer.send({
      topic: 'candlestick-data',
      messages: [
        { value: JSON.stringify(data) }
      ]
    });

    console.log('Sent data:', data);
  }, 1000);
}

produceCandlestickData().catch(console.error);
