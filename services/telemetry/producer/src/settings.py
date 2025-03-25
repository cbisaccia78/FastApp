import os

class Config:
    def __init__(self):
        self.testing = False

        self.kafka_producer_config = {
            'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:9092'),
            'acks': 'all'
        }

config = Config()