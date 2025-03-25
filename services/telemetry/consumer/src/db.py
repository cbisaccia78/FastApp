from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base

engine = create_engine("postgresql://postgres:postgres@db:5432/telemetry")
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
