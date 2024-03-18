from kafka import KafkaConsumer 
import json
import sys 

bootstrap_servers = ['localhost:9092']
topic_name = 'test-topic'
consumer = KafkaConsumer(topic_name, 
                         group_id='group1', 
                         bootstrap_servers=bootstrap_servers, 
                         auto_offset_reset='earliest',
                         enable_auto_commit=True,
                         value_deserializer=lambda value: json.loads(value.decode('utf-8')))

try:
    for message in consumer:
        timestamp = message.value['timestamp']
        content = message.value['content']
        print(f'[{timestamp}] {content}')
except KeyboardInterrupt:
    sys.exit()
