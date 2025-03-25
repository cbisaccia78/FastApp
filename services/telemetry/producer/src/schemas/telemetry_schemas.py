from datetime import datetime
from typing import Dict

from pydantic import BaseModel

class TelemetryEvent(BaseModel):
    user_id: str
    event_type: str
    timestamp: datetime
    metadata: Dict[str, str]