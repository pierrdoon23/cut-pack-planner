from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.models import BaseMaterial, Machine, PackagingType, SeamType, TaskStatus, User, UserRole

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    id: int
    full_name: str
    role: str
    token: Optional[str] = None

class TokenData(BaseModel):
    user_id: int
    role: str

class UserCreate(BaseModel):
    full_name: str
    password: str
    role: UserRole

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None

class UserSchema(BaseModel):
    id: int
    full_name: str
    role: UserRole

    class Config:
        orm_mode = True

# Схемы для основных сущностей
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
    # Пароль должен быть исключен из схемы ответа в реальном приложении

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
    value: Optional[int] = None
    material_used: float
    waste: float

    class Config:
        from_attributes = True

# Схемы для создания/обновления (без ID)
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

class UserCreate(BaseModel):
    full_name: str
    password: str
    role: UserRole

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

    class Config:
        from_attributes = True

class TaskInfoCreate(BaseModel):
    task_id: int
    status: TaskStatus = TaskStatus.PLANNED
    material_used: float
    waste: float

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

class TaskReportSchema(BaseModel):
    id: int
    name: str
    start_time: datetime
    end_time: Optional[datetime] = None

    class Config:
        orm_mode = True

# Новые схемы для создания задачи с расчетом
class TaskCreateWithPieces(BaseModel):
    base_material_id: int
    target_packaging_id: int
    machine_id: int
    user_id: int
    start_time: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: int
    base_material_id: int
    target_packaging_id: int
    machine_id: int
    user_id: int
    start_time: datetime
    status: TaskStatus

    class Config:
        from_attributes = True

class CalculationResponse(BaseModel):
    task_info: Dict[str, Any]
    material_left: float
    cutting_time_minutes: float
    total_target_length: float

    class Config:
        from_attributes = True

class CreateTaskResponse(BaseModel):
    task: TaskResponse
    calculation: CalculationResponse

    class Config:
        from_attributes = True
