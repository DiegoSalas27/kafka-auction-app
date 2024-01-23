from kafka import KafkaConsumer
import json

class MyKafkaConsumer:
    def __init__(self, topic: str, public_ip: str, port: str) -> None:
        self.topic = topic
        self.public_ip = public_ip
        self.port = port

    def getConsumer(self) -> KafkaConsumer:
        consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=f'{self.public_ip}:{self.port}',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

        return consumer