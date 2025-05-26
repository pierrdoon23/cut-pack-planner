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

@router.post("/", response_model=schemas.CreateTaskResponse, status_code=201)
def create_task(task: schemas.TaskCreateWithPieces, db: Session = Depends(database.get_db)):
    try:
        if not task.start_time:
            task.start_time = datetime.utcnow()
        
        # Создаем задачу
        task_create = schemas.TaskCreate(
            base_material_id=task.base_material_id,
            target_packaging_id=task.target_packaging_id,
            machine_id=task.machine_id,
            user_id=task.user_id,
            start_time=task.start_time
        )
        created_task = crud.create_task(db=db, task=task_create)
        
        # Сразу делаем расчет и создаем TaskInfo
        calculation_result = crud.create_task_info_with_calculation(db, created_task.id, task.required_pieces)
        
        return schemas.CreateTaskResponse(
            task=schemas.TaskResponse.model_validate(created_task),
            calculation=schemas.CalculationResponse.model_validate(calculation_result)
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Ошибка создания задачи: {e}")

@router.put("/{task_id}/status", response_model=schemas.Task)
def update_task_status(task_id: int, status: TaskStatus, db: Session = Depends(database.get_db)):
    return crud.update_task_status(db=db, task_id=task_id, status=status)

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
