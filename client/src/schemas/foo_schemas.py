from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field

class FooBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=255)

class FooCreate(FooBase):
    bar_id: int

class FooUpdate(FooBase):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    bar_id: Optional[int]

class FooRead(FooBase):
    id: int
    name: str
    description: str
    bar_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True