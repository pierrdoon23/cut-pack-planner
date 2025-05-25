from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models import PackagingType, SeamType, TaskStatus, UserRole

# --- Схемы для основных сущностей ---
class BaseMaterialSchema(BaseModel):
    id: int
    name: str
    length: float
    width: float
    thickness: float
    package_type: PackagingType

    class Config:
        from_attributes = True

class TargetPackagingSchema(BaseModel):
    id: int
    name: str
    purpose: str
    length: float
    width: float
    package_type: PackagingType
    seam_type: SeamType
    is_two_streams: bool

    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    id: int
    full_name: str
    role: UserRole

    class Config:
        from_attributes = True

class MachineSchema(BaseModel):
    id: int
    name: str
    cutting_speed: float
    machine_width: float

    class Config:
        from_attributes = True

class TaskSchema(BaseModel):
    id: int
    base_material_id: int
    target_packaging_id: int
    user_id: int
    machine_id: int

    class Config:
        from_attributes = True

class TaskInfoSchema(BaseModel):
    id: int
    task_id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PLANNED
    material_used: float
    waste: float

    class Config:
        from_attributes = True

# Для ответа детальной информации по задаче
class Task(BaseModel):
    id: int
    base_material: BaseMaterialSchema
    target_packaging: TargetPackagingSchema
    user: UserSchema
    machine: MachineSchema
    start_time: datetime
    status: TaskStatus

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


# --- Схемы для создания ---
class BaseMaterialCreate(BaseModel):
    name: str
    length: float
    width: float
    thickness: float
    package_type: PackagingType

class TargetPackagingCreate(BaseModel):
    name: str
    purpose: str
    length: float
    width: float
    package_type: PackagingType
    seam_type: SeamType
    is_two_streams: bool

class MachineCreate(BaseModel):
    name: str
    cutting_speed: float
    machine_width: float

class TaskCreate(BaseModel):
    base_material_id: int
    target_packaging_id: int
    user_id: int
    machine_id: int
    status: TaskStatus = TaskStatus.PLANNED
    start_time: Optional[datetime] = None

class TaskInfoCreate(BaseModel):
    task_id: int
    status: TaskStatus = TaskStatus.PLANNED
    material_used: float
    waste: float
