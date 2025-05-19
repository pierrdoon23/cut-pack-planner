from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database
from app.models import TaskStatus

router = APIRouter()

@router.get("/tasks", response_model=list[schemas.TaskSchema], tags=["Tasks"])
def get_all_tasks(db: Session = Depends(database.get_db)):
    return crud.get_tasks(db)

@router.get("/task-info", response_model=list[schemas.TaskInfoSchema], tags=["Tasks"])
def get_all_task_info(db: Session = Depends(database.get_db)):
    return crud.get_tasks(db)

@router.get("/base-materials", response_model=list[schemas.BaseMaterialSchema], tags=["Materials"])
def get_base_materials(db: Session = Depends(database.get_db)):
    return crud.get_base_materials(db)

@router.get("/target-packaging", response_model=list[schemas.TargetPackagingSchema], tags=["Packaging"])
def get_target_packaging(db: Session = Depends(database.get_db)):
    return crud.get_target_packaging(db)

@router.post("/tasks", response_model=schemas.TaskSchema, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    return crud.create_task(db=db, task=task)

@router.put("/tasks/{task_id}/status", tags=["Tasks"])
def update_task_status(task_id: int, status: TaskStatus, db: Session = Depends(database.get_db)):
    return crud.update_task_status(db=db, task_id=task_id, status=status)

@router.get("/machines", response_model=list[schemas.MachineSchema], tags=["Machines"])
def get_machines(db: Session = Depends(database.get_db)):
    return crud.get_machines(db)

