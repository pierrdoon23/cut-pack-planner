from pydantic import BaseModel
from typing import List, Optional

class StatSchema(BaseModel):
    name: str
    value: int
    change: str

    class Config:
        from_attributes = True

class ChartSchema(BaseModel):
    labels: List[str]
    values: List[int]
    colors: Optional[List[str]] = None
