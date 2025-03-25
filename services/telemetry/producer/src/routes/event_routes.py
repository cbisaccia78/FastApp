from flask import Blueprint, request, jsonify

from shared.kafka.kafka_producer import KafkaProducer
from src.schemas.telemetry_schemas import TelemetryEvent
from src.metrics import telemetry_counter
from src.settings import config

event_bp = Blueprint('event_bp', __name__)

producer = KafkaProducer(config.kafka_producer_config)

@event_bp.route('/', methods=['GET'])
def receive_event():
    data = request.get_json()
    try:
        event = TelemetryEvent(**data)
        producer.send_event(event.model_dump(), 'telemetry-events')
        telemetry_counter.inc()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400