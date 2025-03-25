import datetime

from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, DateTime, JSON

Base = declarative_base()

class TelemetryEvent(Base):
    __tablename__ = "telemetry_events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(64))
    event_type: Mapped[str] = mapped_column(String(64))
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime)
    metadata: Mapped[dict] = mapped_column(JSON)
