import json

from confluent_kafka import Consumer
from sqlalchemy.exc import SQLAlchemyError
from dateutil import parser as date_parser

from src.db import Session, init_db
from src.models import TelemetryEvent
from src.settings import config

init_db()

consumer = Consumer(config.kafka_consumer_config)
consumer.subscribe(['telemetry-events'])

print("🟢 Kafka consumer started...")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("❌ Kafka error:", msg.error())
        continue

    try:
        data = json.loads(msg.value().decode("utf-8"))
        event = TelemetryEvent(
            user_id=data["user_id"],
            event_type=data["event_type"],
            timestamp=date_parser.parse(data["timestamp"]),
            metadata=data["metadata"]
        )
        with Session() as session:
            session.add(event)
            session.commit()
        print(f"✅ Stored event: {event.event_type} from {event.user_id}")
    except (KeyError, SQLAlchemyError, Exception) as e:
        print(f"❌ Failed to process event: {e}")