import json
from kafka import KafkaProducer
import sys
from time import sleep 
from datetime import datetime

bootstrap_servers = ['localhost:9092']
topic_name = 'test-topic'
producer = KafkaProducer(bootstrap_servers = bootstrap_servers,
                         value_serializer=lambda value: json.dumps(value).encode('utf-8'))
while True:
    try:
        message = {
            'timestamp': datetime.now().strftime('%H:%M:%S'),
            'content': 'Josef K. is guilty'
        }
        producer.send(topic_name, value=message)
        print(f'[{message["timestamp"]}] Message sent')
        sleep(10)
    except KeyboardInterrupt:
        sys.exit()