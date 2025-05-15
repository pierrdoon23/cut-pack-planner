from sqlalchemy.orm import Session
from app import models

def get_stats(db: Session):
    return db.query(models.Stat).all()

def get_bar_chart_data(db: Session):
    rows = db.query(models.ChartPoint).all()
    labels = [row.label for row in rows]
    values = [row.value for row in rows]
    return {"labels": labels, "values": values}
