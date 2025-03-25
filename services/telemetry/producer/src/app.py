from flask import Flask

from src.settings import config as cfg

from src.routes.event_routes import event_bp
from src.routes.metrics_routes import metrics_bp

def create_app(config=None):
    app = Flask(__name__)

    if config is None:
        config = cfg

    app.register_blueprint(event_bp, url_prefix='/event')
    app.register_blueprint(metrics_bp, url_prefix='/metrics')

    return app

app = create_app()