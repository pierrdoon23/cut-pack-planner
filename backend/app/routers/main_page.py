from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, database

router = APIRouter(prefix="/mainpage", tags=["MainPage"])

@router.get("/rolls_count", tags=["MainPage"])
def get_rolls_count(db: Session = Depends(database.get_db)):
    return crud.get_rolls_count(db)

@router.get("/cutting_maps_count", tags=["MainPage"])
def get_cutting_maps_count(db: Session = Depends(database.get_db)):
    return crud.get_cutting_maps_count(db)

@router.get("/packages_count", tags=["MainPage"])
def get_packages_count(db: Session = Depends(database.get_db)):
    return crud.get_packages_count(db)

@router.get("/bar_chart", tags=["MainPage"])
def get_bar_chart_data(db: Session = Depends(database.get_db)):
    return crud.get_weekly_bar_chart(db)

@router.get("/donut_cutting", tags=["MainPage"])
def get_cutting_donut(db: Session = Depends(database.get_db)):
    return crud.get_cutting_types_donut(db)

@router.get("/donut_usage", tags=["MainPage"])
def get_usage_donut(db: Session = Depends(database.get_db)):
    return crud.get_material_usage_donut(db)
