from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter()

# ---------- /stats ----------
@router.get("/stats", response_model=list[schemas.StatSchema], tags=["Stats"])
def get_stats(db: Session = Depends(database.get_db)):
    return crud.get_stats(db)

# ---------- /bar_chart ----------
@router.get("/bar_chart", tags=["Charts"])
def get_bar_chart(db: Session = Depends(database.get_db)):
    return crud.get_bar_chart_data(db)

# ---------- /donut_cutting ----------
@router.get("/donut_cutting", tags=["Charts"])
def get_donut_cutting():
    return {
        "labels": ["Уголки", "Ленты"],
        "values": [58, 42],
        "colors": ["#66c2a5", "#fc8d62"]
    }

# ---------- /donut_usage ----------
@router.get("/donut_usage", tags=["Charts"])
def get_donut_usage():
    return {
        "labels": ["Использовано", "Отходы"],
        "values": [80, 20],
        "colors": ["green", "red"]
    }
