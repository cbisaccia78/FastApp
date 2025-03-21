from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field

class BarBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=255)

class BarCreate(BarBase):
    pass

class BarUpdate(BarBase):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1, max_length=255)

class BarRead(BarBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True