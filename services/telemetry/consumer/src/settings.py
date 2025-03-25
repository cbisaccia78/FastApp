import os

class Config:
    def __init__(self):
        self.testing = False

        self.kafka_consumer_config = {
            'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'),
            'group.id': os.getenv('KAFKA_GROUP_ID', 'telemetry-consumer-group'),
            'auto.offset.reset': 'earliest'
        }
        
config = Config()