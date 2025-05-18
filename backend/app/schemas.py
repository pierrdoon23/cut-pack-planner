from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class RollSchema(BaseModel):
    id: int
    length: float
    used: float
    wasted: float
    cutting_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class CuttingMapSchema(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PackageSchema(BaseModel):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChartPointSchema(BaseModel):
    id: int
    label: str
    value: int

    class Config:
        from_attributes = True

class CuttingMapDetailSchema(BaseModel):
    id: int
    roll_id: int
    package_id: int
    length: float
    created_at: datetime

    class Config:
        from_attributes = True
