from flask import Flask

from src.database import create_db
from src.settings import config as cfg

from src.routes.foo_routes import foo_bp
from src.routes.bar_routes import bar_bp

def create_app(config=None):
    app = Flask(__name__)
    
    if not config:
        config = cfg

    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

    create_db(app)

    app.register_blueprint(foo_bp, url_prefix='/foos')
    app.register_blueprint(bar_bp, url_prefix='/bars')

    return app

app = create_app()