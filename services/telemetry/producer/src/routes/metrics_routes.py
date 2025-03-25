from flask import Blueprint, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

metrics_bp = Blueprint('metrics_bp', __name__)

@metrics_bp.route('/', methods=['GET'])
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)