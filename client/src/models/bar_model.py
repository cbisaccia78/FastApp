from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from src.database import db

class Bar(db.Model):
    __tablename__ = 'bars'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    foos = relationship('Foo', backref=backref('bar', lazy='joined'))

    def __repr__(self):
        return f'<Bar {self.name}>'