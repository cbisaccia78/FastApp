from typing import Optional

from pydantic import BaseModel, Field

class FooPredictBase(BaseModel):
    foo_id: int = Field(..., title='Task ID')
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=255)

class FooPredictRequest(FooPredictBase):
    pass

class FooPredictResponse(FooPredictBase):
    prediction: float