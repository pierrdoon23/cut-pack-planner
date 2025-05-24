from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Task, TaskInfo, BaseMaterial, TargetPackaging, TaskStatus
from app import schemas
from app import models

# 1. Подсчет рулонов
def get_rolls_count(db: Session):
    total = db.query(BaseMaterial).count()
    last_24h = db.query(BaseMaterial).filter(
        BaseMaterial.id != None,
        BaseMaterial.id.in_(
            db.query(Task.base_material_id).join(TaskInfo)
            .filter(TaskInfo.start_time >= datetime.now(timezone.utc) - timedelta(hours=24))
        )
    ).count()
    return {"total": total, "last_24h": last_24h}


# 2. Подсчет карт раскроя (Tasks)
def get_cutting_maps_count(db: Session):
    total = db.query(Task).count()
    last_24h = db.query(Task).join(TaskInfo)\
        .filter(TaskInfo.start_time >= datetime.now(timezone.utc) - timedelta(hours=24))\
        .count()
    return {"total": total, "last_24h": last_24h}

# 3. Подсчет упаковок
def get_packages_count(db: Session):
    total = db.query(TargetPackaging).count()
    last_24h = db.query(TargetPackaging).filter(
        TargetPackaging.id.in_(
            db.query(Task.target_packaging_id).join(TaskInfo)
            .filter(TaskInfo.start_time >= datetime.now(timezone.utc) - timedelta(hours=24))
        )
    ).count()
    return {"total": total, "last_24h": last_24h}

# 4. График заказов за неделю
def get_weekly_bar_chart(db: Session):
    labels = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    today = datetime.now(timezone.utc)
    start_of_week = today - timedelta(days=today.weekday())
    
    values = []
    for i in range(7):
        day_start = start_of_week + timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        count = db.query(TaskInfo).filter(TaskInfo.start_time >= day_start, TaskInfo.start_time < day_end).count()
        values.append(count)
    
    return {"labels": labels, "values": values}

# 5. Типы нарезки
def get_cutting_types_donut(db: Session):
    query = db.query(
        TargetPackaging.seam_type,
        func.count(Task.id).label("count")
    ).join(Task, Task.target_packaging_id == TargetPackaging.id)\
     .group_by(TargetPackaging.seam_type)\
     .all()

    total = sum(item.count for item in query)
    result = [{"type": seam.name, "percent": round(item.count / total * 100, 1)} for seam, item in zip([i[0] for i in query], query)]
    return result if result else [{"type": "N/A", "percent": 100}]

# 6. Использование и отходы
def get_material_usage_donut(db: Session):
    used_sum = db.query(func.sum(TaskInfo.material_used)).scalar() or 0
    waste_sum = db.query(func.sum(TaskInfo.waste)).scalar() or 0
    total = used_sum + waste_sum
    if total == 0:
        return {"used_percent": 0, "wasted_percent": 0}
    return {
        "used_percent": round(used_sum / total * 100, 1),
        "wasted_percent": round(waste_sum / total * 100, 1)
    }


#----------------------визуал картыв

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_all_tasks(db: Session):
    return db.query(models.Task).all()

def get_task_info(db: Session):
    tasks = db.query(models.Task).all()
    result = []
    for task in tasks:
        task_info = db.query(models.TaskInfo).filter(models.TaskInfo.task_id == task.id).first()
        result.append({
            "task_id": task.id,
            "status": task.status,
            "start_time": task.start_time,
            "end_time": task_info.end_time if task_info else None,
            "material_used": float(task_info.material_used) if task_info else None,
            "waste": float(task_info.waste) if task_info else None,
            "base_material": {
                "name": task.base_material.name,
                "length": task.base_material.length,
                "width": task.base_material.width,
                "thickness": task.base_material.thickness,
                "package_type": task.base_material.package_type
            },
            "target_packaging": {
                "name": task.target_packaging.name,
                "purpose": task.target_packaging.purpose,
                "length": task.target_packaging.length,
                "width": task.target_packaging.width,
                "package_type": task.target_packaging.package_type,
                "seam_type": task.target_packaging.seam_type,
                "is_two_streams": task.target_packaging.is_two_streams
            },
            "machine": {
                "name": task.machine.name,
                "cutting_speed": task.machine.cutting_speed,
                "machine_width": task.machine.machine_width
            },
            "user": {
                "name": task.user.full_name,
                "role": task.user.role
            }
        })
    return result

def get_base_materials(db: Session):
    return db.query(models.BaseMaterial).all()

def get_cutting_maps(db: Session):
    return db.query(models.Task).all()

def get_target_packaging(db: Session):
    return db.query(models.TargetPackaging).all()

def get_machines(db: Session):
    return db.query(models.Machine).all()

def update_task_status(db: Session, task_id: int, status: TaskStatus):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise Exception("Задача не найдена")
    task.status = status
    db.commit()
    db.refresh(task)
    return task