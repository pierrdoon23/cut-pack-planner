from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import List

router = APIRouter(prefix="/creation", tags=["Creation"])

# --- GET Base Materials ---
@router.get("/base_materials", response_model=List[schemas.BaseMaterialSchema])
def read_base_materials(db: Session = Depends(get_db)):
    return db.query(models.BaseMaterial).all()

# --- GET Target Packaging ---
@router.get("/target_packaging", response_model=List[schemas.TargetPackagingSchema])
def read_target_packaging(db: Session = Depends(get_db)):
    return db.query(models.TargetPackaging).all()

# --- GET Machines ---
@router.get("/machines", response_model=List[schemas.MachineSchema])
def read_machines(db: Session = Depends(get_db)):
    return db.query(models.Machine).all()

# --- GET Tasks (for UI refresh) ---
@router.get("/tasks", response_model=List[schemas.Task])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

# --- POST Task (from UI) ---
@router.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    base_material = db.query(models.BaseMaterial).filter_by(id=task.base_material_id).first()
    target_packaging = db.query(models.TargetPackaging).filter_by(id=task.target_packaging_id).first()
    user = db.query(models.User).filter_by(id=task.user_id).first()
    machine = db.query(models.Machine).filter_by(id=task.machine_id).first()

    if not all([base_material, target_packaging, user, machine]):
        raise HTTPException(status_code=400, detail="Некорректные ID материалов, станка или пользователя")

    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# --- BaseMaterial ---
@router.post("/base_materials", response_model=schemas.BaseMaterialSchema)
def create_base_material(material: schemas.BaseMaterialCreate, db: Session = Depends(get_db)):
    # Check if material with this name already exists
    existing_material = db.query(models.BaseMaterial).filter(models.BaseMaterial.name == material.name).first()
    if existing_material:
        raise HTTPException(status_code=400, detail=f"Материал с названием '{material.name}' уже существует")
    
    db_material = models.BaseMaterial(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

# --- TargetPackaging ---
@router.post("/target_packaging", response_model=schemas.TargetPackagingSchema)
def create_target_packaging(packaging: schemas.TargetPackagingCreate, db: Session = Depends(get_db)):
    db_packaging = models.TargetPackaging(**packaging.dict())
    db.add(db_packaging)
    db.commit()
    db.refresh(db_packaging)
    return db_packaging

# --- User ---
@router.post("/users", response_model=schemas.UserSchema)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Machine ---
@router.post("/machines", response_model=schemas.MachineSchema)
def create_machine(machine: schemas.MachineCreate, db: Session = Depends(get_db)):
    db_machine = models.Machine(**machine.dict())
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine

# --- Task ---
@router.post("/tasks", response_model=schemas.TaskSchema)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

# --- TaskInfo ---
@router.post("/task_info", response_model=schemas.TaskInfoSchema)
def create_task_info(info: schemas.TaskInfoCreate, db: Session = Depends(get_db)):
    db_info = models.TaskInfo(**info.dict(), start_time=datetime.now(timezone.utc))
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info

@router.delete("/base_materials/{material_id}")
def delete_base_material(material_id: int, db: Session = Depends(get_db)):
    # Проверяем, есть ли связанные задачи
    related_tasks = db.query(models.Task).filter(models.Task.base_material_id == material_id).first()
    if related_tasks:
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить материал, так как он используется в задачах"
        )
    
    material = db.query(models.BaseMaterial).filter(models.BaseMaterial.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Материал не найден")
    
    db.delete(material)
    db.commit()
    return {"message": "Материал успешно удален"}

@router.delete("/machines/{machine_id}")
def delete_machine(machine_id: int, db: Session = Depends(get_db)):
    # Проверяем, есть ли связанные задачи
    related_tasks = db.query(models.Task).filter(models.Task.machine_id == machine_id).first()
    if related_tasks:
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить станок, так как он используется в задачах"
        )
    
    machine = db.query(models.Machine).filter(models.Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Станок не найден")
    
    db.delete(machine)
    db.commit()
    return {"message": "Станок успешно удален"}

@router.delete("/target_packaging/{package_id}")
def delete_target_packaging(package_id: int, db: Session = Depends(get_db)):
    # Проверяем, есть ли связанные задачи
    related_tasks = db.query(models.Task).filter(models.Task.target_packaging_id == package_id).first()
    if related_tasks:
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить упаковку, так как она используется в задачах"
        )
    
    packaging = db.query(models.TargetPackaging).filter(models.TargetPackaging.id == package_id).first()
    if not packaging:
        raise HTTPException(status_code=404, detail="Упаковка не найдена")
    
    db.delete(packaging)
    db.commit()
    return {"message": "Упаковка успешно удалена"}

