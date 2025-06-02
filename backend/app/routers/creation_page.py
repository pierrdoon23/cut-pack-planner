from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, crud
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
    return crud.create_base_material(db, material)

@router.delete("/base_materials/{material_id}")
def delete_base_material(material_id: int, db: Session = Depends(get_db)):
    return crud.delete_base_material(db, material_id)

# --- TargetPackaging ---
@router.post("/target_packaging", response_model=schemas.TargetPackagingSchema)
def create_target_packaging(packaging: schemas.TargetPackagingCreate, db: Session = Depends(get_db)):
    return crud.create_target_packaging(db, packaging)

@router.delete("/target_packaging/{packaging_id}")
def delete_target_packaging(packaging_id: int, db: Session = Depends(get_db)):
    return crud.delete_target_packaging(db, packaging_id)

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
    return crud.create_machine(db, machine)

@router.delete("/machines/{machine_id}")
def delete_machine(machine_id: int, db: Session = Depends(get_db)):
    machine = db.query(models.Machine).filter(models.Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Станок не найден")
    
    # Проверяем, используется ли станок в задачах
    task_exists = db.query(models.Task).filter(models.Task.machine_id == machine_id).first()
    if task_exists:
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить станок, так как он используется в задачах"
        )
    
    db.delete(machine)
    db.commit()
    return {"message": "Станок успешно удален"}

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

