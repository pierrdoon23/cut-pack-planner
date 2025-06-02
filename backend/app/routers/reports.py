from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import get_task_report_data

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/tasks")
def get_report_tasks(db: Session = Depends(get_db)):
    return get_task_report_data(db)
