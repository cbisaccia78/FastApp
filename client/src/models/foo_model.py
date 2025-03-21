from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.sql import func

from src.database import db

class Foo(db.Model):
    __tablename__ = 'foos'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    
    bar_id = Column(Integer, ForeignKey('bars.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<Foo {self.name}>'