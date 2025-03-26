import threading
import requests
import json
from concurrent.futures import ThreadPoolExecutor

from confluent_kafka import Consumer

from src.settings import config

class FooCreatedConsumer:
    """
    FooCreatedConsumer is responsible for consuming foo-created events from a Kafka topic 
    and asynchronously estimating them by calling an api in the model service
    .
    Attributes:
        continue_running (bool): A flag to control the running state of the worker.
        lock (threading.Lock): A lock to synchronize access to shared resources.
        executor (ThreadPoolExecutor): A thread pool executor to handle asynchronous foo estimation.
    Methods:
        __init__():
            Initializes the FooCreatedConsumer with default settings.
        start():
            Starts the worker to consume foos from the 'foo-created' Kafka topic and
            submit them for estimation.
        predict_foo(foo_id, foo):
            Sends a POST request to an external service to predict the given foo.
        stop():
            Stops the worker and shuts down the thread pool executor.
    """
    ESTIMATE_URL = f'http://localhost:5001/models/foo'

    def __init__(self):
        self.continue_running = False
        self.lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=5)  # Adjust the number of workers as needed

    def start(self):
        consumer = Consumer(config.kafka_consumer_config)
        consumer.subscribe(['foo-created'])

        with self.lock:
            self.continue_running = True

        while True:
            with self.lock:
                if not self.continue_running:
                    break

            event = consumer.poll(1.0)

            if event is None:
                continue
            if event.error():
                print(f'Consumer error: {event.error()}')
                continue

            foo_id = event.key().decode('utf-8')
            foo = event.value().decode('utf-8')

            print(f'Message: {event.value()}')

            # Asynchronously call the update_foo route
            self.executor.submit(self.predict_foo, foo_id, foo)

        consumer.close()
    
    def predict_foo(self, foo_id, foo):

        foo = json.loads(foo)
        data = {
            'foo_id': foo_id,
            'name': foo['name'],
            'description': foo['description']
        }
        try:
            response = requests.post(self.ESTIMATE_URL, json=data)

            if response.status_code == 201:
                print(f'Successfully predictd {foo_id}')
            else:
                print(f'Failed to predict foo {foo_id}: {response.status_code} {response.text}')
        except requests.RequestException as e:
            print(f'Error updating foo {foo_id}: {e}')
    
    def stop(self):
        with self.lock:
            self.continue_running = False
        self.executor.shutdown(wait=True)

    

    

    