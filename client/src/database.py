from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

#migrate = Migrate()

def create_db(app: Flask) -> None:
    db.init_app(app)

    with app.app_context():
        db.create_all()
    
    #migrate.init_app(app, db)