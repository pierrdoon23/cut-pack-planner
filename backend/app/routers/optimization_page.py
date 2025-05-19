from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, database, schemas
from app.database import get_db
from app.models import CuttingMap

router = APIRouter()


@router.get("/cutting-maps")
def get_cutting_maps(db: Session = Depends(get_db)):
    maps = db.query(CuttingMap).order_by(CuttingMap.created_at.desc()).all()
    return [{"id": m.id, "created_at": m.created_at.isoformat()} for m in maps]

@router.post("/select", tags=["Optimization"])
def select_source(roll: schemas.OptimizationRollSchema, db: Session = Depends(database.get_db)):
    return crud.add_roll(db, roll, roll_type="source")

@router.post("/set", tags=["Optimization"])
def set_target(roll: schemas.OptimizationRollSchema, db: Session = Depends(database.get_db)):
    return crud.add_roll(db, roll, roll_type="target")

@router.get("/optimize", response_model=schemas.OptimizationResultSchema, tags=["Optimization"])
def optimize(db: Session = Depends(database.get_db)):
    result = crud.run_cutting_optimization(db)
    return schemas.OptimizationResultSchema(**result)

