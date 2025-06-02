from datetime import datetime
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, database
from app.models import TaskStatus
from pydantic import BaseModel
import traceback

class TaskCreateWithPieces(BaseModel):
    base_material_id: int
    target_packaging_id: int
    machine_id: int
    user_id: int
    required_pieces: int
    start_time: datetime = None

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

class TaskStatusUpdate(BaseModel):
    status: TaskStatus

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

@router.post("/", response_model=schemas.CreateTaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    try:
        created_task = crud.create_task(db=db, task=task)
        task_info = crud.get_task_info(db, created_task.id)
        
        if not task_info:
            raise HTTPException(status_code=500, detail="Failed to get task info")

        return {
            "task": created_task,
            "calculation": {
                "task_info": task_info,
                "material_left": task_info.get("material_used", 0),
                "cutting_time_minutes": 0,
                "total_target_length": task_info.get("material_used", 0)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{task_id}/status", response_model=schemas.Task)
def update_task_status(task_id: int, status_update: TaskStatusUpdate, db: Session = Depends(database.get_db)):
    return crud.update_task_status(db=db, task_id=task_id, status=status_update.status)

@router.get("/machines", response_model=List[schemas.MachineSchema])
def get_machines(db: Session = Depends(database.get_db)):
    return crud.get_machines(db)

@router.post("/{task_id}/calculate")
def calculate_task(
    task_id: int,
    required_pieces: int,
    db: Session = Depends(database.get_db)
):
    """
    Создает расчет для задачи с указанным количеством штук
    """
    try:
        result = crud.create_task_info_with_calculation(db, task_id, required_pieces)
        return result
    except HTTPException as e:
        raise e
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(database.get_db)):
    try:
        crud.delete_task(db, task_id)
        return {"message": f"Задача {task_id} удалена"}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка удаления: {e}")
