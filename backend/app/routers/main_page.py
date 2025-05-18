from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter()

# ---------- /rolls_count ----------
@router.get("/rolls_count", tags=["MainPage"])
def get_rolls_count(db: Session = Depends(database.get_db)):
    return crud.get_rolls_count(db)

# ---------- /cutting_maps_count ----------
@router.get("/cutting_maps_count", tags=["MainPage"])
def get_cutting_maps_count(db: Session = Depends(database.get_db)):
    return crud.get_cutting_maps_count(db)

# ---------- /packages_count ----------
@router.get("/packages_count", tags=["MainPage"])
def get_packages_count(db: Session = Depends(database.get_db)):
    return crud.get_packages_count(db)

# ---------- /bar_chart ----------
@router.get("/bar_chart", tags=["Charts"])
def get_bar_chart(db: Session = Depends(database.get_db)):
    return crud.get_bar_chart_data(db)

# ---------- /donut_cutting ----------
@router.get("/donut_cutting", tags=["Charts"])
def get_donut_cutting(db: Session = Depends(database.get_db)):
    return crud.get_cutting_types_data(db)

# ---------- /donut_usage ----------
@router.get("/donut_usage", tags=["Charts"])
def get_donut_usage(db: Session = Depends(database.get_db)):
    return crud.get_usage_waste_data(db)
