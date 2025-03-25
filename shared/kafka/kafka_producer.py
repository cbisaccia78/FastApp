import json

from confluent_kafka import Producer

class KafkaProducer:
    def __init__(self, config: dict):
        self.producer = producer = Producer(config)

    def send_event(self, event: dict, topic: str):
        self.producer.produce(topic, json.dumps(event).encode("utf-8"))
        self.producer.flush()