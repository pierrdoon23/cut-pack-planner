from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, DateTime, DECIMAL, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from app.database import Base

class UserRole(str, Enum):
    ADMIN = "admin"
    OPERATOR = "operator"

class TaskStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class PackagingType(str, Enum):
    VACUUM = "vacuum"
    FLOW_PACK = "flow_pack"
    SHRINK = "shrink"

class SeamType(str, Enum):
    DOUBLE_SEAM = "double_seam"
    SINGLE_SEAM = "single_seam"
    ULTRASONIC = "ultrasonic"

class BaseMaterial(Base):
    __tablename__ = "base_materials"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)
    length = Column(Float)  # в метрах
    width = Column(Float)   # в метрах
    thickness = Column(Float)
    package_type = Column(SQLAlchemyEnum(PackagingType))

class TargetPackaging(Base):
    __tablename__ = "target_packaging"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    purpose = Column(String(255))
    length = Column(Float)
    width = Column(Float)
    package_type = Column(SQLAlchemyEnum(PackagingType))
    seam_type = Column(SQLAlchemyEnum(SeamType))
    is_two_streams = Column(Boolean)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    full_name = Column(String(150))
    password = Column(String(255))
    role = Column(SQLAlchemyEnum(UserRole))

class Machine(Base):
    __tablename__ = "machines"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    cutting_speed = Column(Float)  # м/мин
    machine_width = Column(Float)  # максимальная ширина обработки

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    base_material_id = Column(Integer, ForeignKey("base_materials.id"))
    target_packaging_id = Column(Integer, ForeignKey("target_packaging.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    machine_id = Column(Integer, ForeignKey("machines.id"))
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.PLANNED)
    start_time = Column(DateTime, default=datetime.utcnow)

    base_material = relationship("BaseMaterial")
    target_packaging = relationship("TargetPackaging")
    user = relationship("User")
    machine = relationship("Machine")

class TaskInfo(Base):
    __tablename__ = "task_info"
    
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.PLANNED)
    value = Column(Integer)
    material_used = Column(DECIMAL(10, 2))  # в метрах
    waste = Column(DECIMAL(10, 2))         # в метрах
    
    task = relationship("Task")