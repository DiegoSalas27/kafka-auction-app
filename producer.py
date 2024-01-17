from kafka import KafkaProducer
import time
import json
import random

class MyKafkaProducer:
    def __init__(self, topic: str, public_ip: str, port: str) -> None:
        self.topic = topic
        self.public_ip = public_ip
        self.port = port

    def produce(self) -> None:
        producer = KafkaProducer(
            bootstrap_servers=f'{self.public_ip}:{self.port}',
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        while True:
            data = {
                'timestamp': time.time(),
                'value': random.randint(1, 100)
            }
            print(f"Producing data: {data}")
            producer.send(self.topic, value=data)
            time.sleep(1)
