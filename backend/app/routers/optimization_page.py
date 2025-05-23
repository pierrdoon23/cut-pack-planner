from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database
from app.models import TaskStatus
import traceback

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", response_model=List[schemas.Task])
def get_tasks(db: Session = Depends(database.get_db)):
    return crud.get_all_tasks(db)

@router.get("/info", response_model=List[dict])
def get_task_info(db: Session = Depends(database.get_db)):
    return crud.get_task_info(db)

@router.get("/base-materials", response_model=List[schemas.BaseMaterialSchema])
def get_base_materials(db: Session = Depends(database.get_db)):
    return crud.get_base_materials(db)

@router.get("/cutting-maps", response_model=List[schemas.Task])
def get_cutting_maps(db: Session = Depends(database.get_db)):
    return crud.get_cutting_maps(db)

@router.get("/target-packaging", response_model=List[schemas.TargetPackagingSchema])
def get_target_packaging(db: Session = Depends(database.get_db)):
    return crud.get_target_packaging(db)

@router.post("/", response_model=schemas.Task, status_code=201)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    try:
        if not task.start_time:
            task.start_time = datetime.utcnow()
        return crud.create_task(db=db, task=task)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка создания задачи: {e}")

@router.put("/{task_id}/status", response_model=schemas.Task)
def update_task_status(task_id: int, status: TaskStatus, db: Session = Depends(database.get_db)):
    return crud.update_task_status(db=db, task_id=task_id, status=status)

@router.get("/machines", response_model=List[schemas.MachineSchema])
def get_machines(db: Session = Depends(database.get_db)):
    return crud.get_machines(db)
