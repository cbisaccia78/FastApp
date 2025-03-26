import json
import requests

from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from confluent_kafka import Producer

from src.schemas.model_schemas import FooPredictRequest
from src.settings import config

# Here, we use the service name "tf-serving" (as defined in docker-compose)
# and port 8501 as mapped in docker-compose.
TF_SERVING_URL = "http://tf-serving:8501/v1/models/codebert_regression_model:predict"

if not config.testing:
    producer = Producer(config.kafka_producer_config)

model_bp = Blueprint('model_bp', __name__)

@model_bp.route('/foo', methods=['POST'])
def predict_foo():
    try:
        data = request.get_json()
        foo = FooPredictRequest(**data)
    except ValidationError as e:
        print(e.errors())
        return jsonify({'error': e.errors()}), 422


    names, descriptions = [foo.name], [foo.description]
    
    # Build payload for TensorFlow Serving.
    payload = {
        "instances": [
            {
                "name_input": names.numpy().tolist(),
                "desc_input": descriptions.numpy().tolist()
            }
        ]
    }
    
    try:
        resp = requests.post(TF_SERVING_URL, json=payload)
        resp.raise_for_status()
        prediction = resp.json()
    except Exception as e:
        return jsonify({'error': f"TF Serving request failed: {str(e)}"}), 500

    # Build response predict, including additional info if needed.
    ret = foo.model_dump()
    # Parse the prediction output.
    # (Assuming the prediction comes as {"predictions": [[pred_value]]})
    try:
        prediction = prediction["predictions"][0][0]
    except (KeyError, IndexError):
        return jsonify({'error': "Unexpected response structure from TF Serving"}), 500

    ret["prediction"] = prediction

    if not config.testing:
        # Produce an event on Kafka
        producer.produce('predict-complete', key=str(ret['foo_id']), value=json.dumps(ret))
        producer.flush()

    return jsonify(ret), 201