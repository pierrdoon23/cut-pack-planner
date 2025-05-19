from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Date
from app import models
from datetime import datetime, timedelta
from app.schemas import OptimizationRollSchema

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

# ----visual/карты 
# Source/Target rolls для раскроя

def add_roll(db: Session, roll: OptimizationRollSchema, roll_type: str):
    new_roll = models.Roll(
        length=roll.length,
        used=0,
        wasted=0,
        cutting_type=roll_type,
        created_at=datetime.utcnow()
    )
    db.add(new_roll)
    db.commit()
    db.refresh(new_roll)
    return new_roll

def get_rolls_by_type(db: Session, roll_type: str):
    return db.query(models.Roll).filter(models.Roll.cutting_type == roll_type).all()

def run_cutting_optimization(db: Session):
    sources = get_rolls_by_type(db, "source")
    targets = get_rolls_by_type(db, "target")

    if not sources or not targets:
        return {"efficiency": 0.0, "waste": 0.0}

    # Сортировка по убыванию
    sources = sorted(sources, key=lambda r: r.length, reverse=True)
    targets = sorted(targets, key=lambda r: r.length, reverse=True)

    # Преобразуем источники в список остатка
    source_lengths = [r.length for r in sources]
    waste_total = 0
    used_total = 0

    for target in targets:
        placed = False
        for i in range(len(source_lengths)):
            if source_lengths[i] >= target.length:
                source_lengths[i] -= target.length
                used_total += target.length
                placed = True
                break
        if not placed:
            # Если никуда не влезает — считаем "отказ"
            waste_total += target.length

    # Остатки — отходы
    waste_total += sum(source_lengths)

    total_input = sum(r.length for r in sources)
    efficiency = used_total / total_input if total_input > 0 else 0.0

    return {
        "efficiency": round(efficiency * 100, 2),
        "waste": round(waste_total, 2)
    }
