from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from app import models
from datetime import datetime, timedelta

# Количество и динамика за 24ч

def get_rolls_count(db: Session):
    total = db.query(func.count(models.Roll.id)).scalar()
    last_24h = db.query(func.count(models.Roll.id)).filter(models.Roll.created_at >= datetime.utcnow() - timedelta(days=1)).scalar()
    return {"total": total, "last_24h": last_24h}

def get_cutting_maps_count(db: Session):
    total = db.query(func.count(models.CuttingMap.id)).scalar()
    last_24h = db.query(func.count(models.CuttingMap.id)).filter(models.CuttingMap.created_at >= datetime.utcnow() - timedelta(days=1)).scalar()
    return {"total": total, "last_24h": last_24h}

def get_packages_count(db: Session):
    total = db.query(func.count(models.Package.id)).scalar()
    last_24h = db.query(func.count(models.Package.id)).filter(models.Package.created_at >= datetime.utcnow() - timedelta(days=1)).scalar()
    return {"total": total, "last_24h": last_24h}

# Барчарт по дням недели (количество рулонов)
def get_bar_chart_data(db: Session):
    # Для PostgreSQL: 0=Воскресенье, 1=Понедельник, ..., 6=Суббота
    rows = db.query(
        func.extract('dow', models.Roll.created_at).label('weekday'),
        func.count(models.Roll.id)
    ).group_by('weekday').order_by('weekday').all()
    # Преобразуем номера дней в русские сокращения
    week_map = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
    labels = [week_map[int(r[0])] for r in rows]
    values = [r[1] for r in rows]
    return {"labels": labels, "values": values}

# Типы нарезки (проценты)
def get_cutting_types_data(db: Session):
    total = db.query(func.count(models.Roll.id)).scalar() or 1
    rows = db.query(models.Roll.cutting_type, func.count(models.Roll.id)).group_by(models.Roll.cutting_type).all()
    return [
        {"type": r[0], "percent": round(r[1] / total * 100, 1)}
        for r in rows
    ]

# Использовано/отходы (проценты)
def get_usage_waste_data(db: Session):
    used = db.query(func.sum(models.Roll.used)).scalar() or 0
    wasted = db.query(func.sum(models.Roll.wasted)).scalar() or 0
    total = used + wasted or 1
    return {
        "used_percent": round(used / total * 100, 1),
        "wasted_percent": round(wasted / total * 100, 1)
    }
