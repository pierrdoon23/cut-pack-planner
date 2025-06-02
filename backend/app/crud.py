from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Task, TaskInfo, BaseMaterial, TargetPackaging, TaskStatus, User
from app import models, schemas

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.full_name == username).first()
    if not user or user.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль"
        )
    return user

def get_user(db: Session, user_id: int) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_name(db: Session, full_name: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.full_name == full_name).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(
        full_name=user.full_name,
        password=user.password,  # В реальном приложении хэшируйте пароль
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    db_user = get_user(db, user_id)
    if db_user is None:
        return None
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    try:
        db_user = get_user(db, user_id)
        if db_user is None:
            return False

        # Находим все задачи пользователя
        user_tasks = db.query(Task).filter(Task.user_id == user_id).all()
        
        # Удаляем информацию о задачах и сами задачи
        for task in user_tasks:
            task_info = db.query(TaskInfo).filter(TaskInfo.task_id == task.id).first()
            if task_info:
                db.delete(task_info)
            db.delete(task)
        
        # Удаляем пользователя
        db.delete(db_user)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ошибка при удалении пользователя: {str(e)}"
        )

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
    
    # Получаем начало текущей недели (понедельник)
    start_of_week = today - timedelta(days=today.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    
    print(f"Today: {today}")
    print(f"Start of week: {start_of_week}")
    
    values = []
    for i in range(7):
        day_start = start_of_week + timedelta(days=i)
        day_end = day_start + timedelta(days=1)
        
        # Получаем все задачи за день для отладки
        tasks = db.query(Task).join(TaskInfo).filter(
            TaskInfo.end_time >= day_start,
            TaskInfo.end_time < day_end,
            Task.status == 'completed'
        ).all()
        
        print(f"\nDay {i+1} ({day_start.date()}):")
        for task in tasks:
            task_info = db.query(TaskInfo).filter(TaskInfo.task_id == task.id).first()
            print(f"Task {task.id}: status={task.status}, end_time={task_info.end_time if task_info else None}")
        
        count = len(tasks)
        values.append(count)
        print(f"Count for day {i+1}: {count}")
    
    result = {"labels": labels, "values": values}
    print(f"\nFinal result: {result}")
    return result

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

def create_task_info_with_calculation(db: Session, task_id: int):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    base = task.base_material
    target = task.target_packaging
    machine = task.machine

    streams = 2 if target.is_two_streams else 1
    per_stream_width = target.width * streams

    if per_stream_width > machine.machine_width:
        raise HTTPException(status_code=400, detail="Ширина не влезает в машину")

    # Максимально возможное количество упаковок
    total_available_length = base.length
    estimated_pieces = int(total_available_length / target.length)

    material_used = estimated_pieces * target.length
    waste = material_used * 0.02
    cutting_time_minutes = material_used / machine.cutting_speed
    end_time = datetime.utcnow() + timedelta(minutes=cutting_time_minutes)

    task_info = models.TaskInfo(
        task_id=task.id,
        start_time=datetime.utcnow(),
        end_time=end_time,
        material_used=round(material_used, 2),
        waste=round(waste, 2),
        status=TaskStatus.PLANNED,
    )

    db.add(task_info)
    db.commit()
    db.refresh(task_info)

    return {
        "task_info": task_info,
        "required_pieces": estimated_pieces,
        "cutting_time_minutes": round(cutting_time_minutes, 2),
        "material_used": round(material_used, 2),
        "waste": round(waste, 2)
    }


def get_all_tasks(db: Session):
    return db.query(models.Task).all()

def get_task_info(db: Session, task_id: int = None):
    if task_id is not None:
        task = db.query(models.Task).filter(models.Task.id == task_id).first()
        if not task:
            return None
        task_info = db.query(models.TaskInfo).filter(models.TaskInfo.task_id == task_id).first()
        return {
            "task_id": task.id,
            "status": task.status,
            "start_time": task.start_time,
            "end_time": task_info.end_time if task_info else None,
            "material_used": float(task_info.material_used) if task_info else None,
            "waste": float(task_info.waste) if task_info else None,
            "value": task_info.value if task_info else None,
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
        }
    else:
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
                "value": task_info.value if task_info else None,
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
    
    # Если задача завершена, обновляем end_time в TaskInfo
    if status == 'completed':
        task_info = db.query(models.TaskInfo).filter(models.TaskInfo.task_id == task_id).first()
        if task_info:
            current_time = datetime.now(timezone.utc)
            print(f"Setting end_time for task {task_id} to {current_time}")
            task_info.end_time = current_time
            task_info.status = status
        else:
            print(f"No TaskInfo found for task {task_id}")
    
    db.commit()
    db.refresh(task)
    return task


# В crud.py
def create_base_material(db: Session, material: schemas.BaseMaterialCreate):
    db_material = models.BaseMaterial(**material.dict())
    db.add(db_material)
    db.commit()
    db.refresh(db_material)
    return db_material

def create_target_packaging(db: Session, packaging: schemas.TargetPackagingCreate):
    db_packaging = models.TargetPackaging(**packaging.dict())
    db.add(db_packaging)
    db.commit()
    db.refresh(db_packaging)
    return db_packaging

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())  # В реальности — хешируй пароль!
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_machine(db: Session, machine: schemas.MachineCreate):
    db_machine = models.Machine(**machine.dict())
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine

def create_task_info(db: Session, info: schemas.TaskInfoCreate):
    db_info = models.TaskInfo(**info.dict(), start_time=datetime.utcnow())
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return db_info

def get_task_report_data(db: Session):
    tasks = db.query(models.Task).outerjoin(models.TaskInfo).all()
    result = []

    for task in tasks:
        task_info = db.query(models.TaskInfo).filter(models.TaskInfo.task_id == task.id).first()
        result.append({
            "id": task.id,
            "name": f"Задача {task.id}",
            "start_time": task_info.start_time if task_info else None,
            "end_time": task_info.end_time if task_info else None
        })

    return result

def delete_task(db: Session, task_id: int):
    # Сначала удаляем связанную информацию о задаче
    task_info = db.query(models.TaskInfo).filter(models.TaskInfo.task_id == task_id).first()
    if task_info:
        db.delete(task_info)
        db.commit()

    # Затем удаляем саму задачу
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    db.delete(task)
    db.commit()

def create_task(db: Session, task: schemas.TaskCreate):
    # Получаем базовый материал и целевую упаковку
    base_material = db.query(models.BaseMaterial).filter(models.BaseMaterial.id == task.base_material_id).first()
    target_packaging = db.query(models.TargetPackaging).filter(models.TargetPackaging.id == task.target_packaging_id).first()
    machine = db.query(models.Machine).filter(models.Machine.id == task.machine_id).first()
    
    if not base_material or not target_packaging or not machine:
        raise HTTPException(status_code=404, detail="Материал, упаковка или станок не найдены")

    # Рассчитываем количество штук
    total_available_length = base_material.length
    estimated_pieces = int(total_available_length / target_packaging.length)

    # Создаем задачу
    db_task = models.Task(
        base_material_id=task.base_material_id,
        target_packaging_id=task.target_packaging_id,
        machine_id=task.machine_id,
        user_id=task.user_id,
        start_time=task.start_time or datetime.utcnow(),
        status=task.status
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    # Рассчитываем время выполнения
    material_used = estimated_pieces * target_packaging.length
    waste = material_used * 0.02  # 2% отходов
    cutting_time_minutes = material_used / machine.cutting_speed
    end_time = datetime.utcnow() + timedelta(minutes=cutting_time_minutes)

    # Создаем информацию о задаче
    task_info = models.TaskInfo(
        task_id=db_task.id,
        start_time=datetime.utcnow(),
        end_time=end_time,
        material_used=round(material_used, 2),
        waste=round(waste, 2),
        status=task.status,
        value=estimated_pieces  # Сохраняем рассчитанное количество штук
    )
    db.add(task_info)
    db.commit()
    db.refresh(task_info)

    return db_task

def delete_base_material(db: Session, material_id: int):
    # Проверяем существование материала
    material = db.query(models.BaseMaterial).filter(models.BaseMaterial.id == material_id).first()
    if not material:
        raise HTTPException(status_code=404, detail="Материал не найден")
    
    # Проверяем, используется ли материал в задачах
    task_exists = db.query(models.Task).filter(models.Task.base_material_id == material_id).first()
    if task_exists:
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить материал, так как он используется в задачах"
        )
    
    try:
        db.delete(material)
        db.commit()
        return {"message": "Материал успешно удален"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при удалении материала: {str(e)}"
        )

def delete_target_packaging(db: Session, packaging_id: int):
    # Проверяем существование упаковки
    packaging = db.query(models.TargetPackaging).filter(models.TargetPackaging.id == packaging_id).first()
    if not packaging:
        raise HTTPException(status_code=404, detail="Упаковка не найдена")
    
    # Проверяем, используется ли упаковка в задачах
    task_exists = db.query(models.Task).filter(models.Task.target_packaging_id == packaging_id).first()
    if task_exists:
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить упаковку, так как она используется в задачах"
        )
    
    try:
        db.delete(packaging)
        db.commit()
        return {"message": "Упаковка успешно удалена"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при удалении упаковки: {str(e)}"
        )

def delete_machine(db: Session, machine_id: int):
    # Проверяем существование станка
    machine = db.query(models.Machine).filter(models.Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Станок не найден")
    
    # Проверяем, используется ли станок в задачах
    task_exists = db.query(models.Task).filter(models.Task.machine_id == machine_id).first()
    if task_exists:
        raise HTTPException(
            status_code=400,
            detail="Невозможно удалить станок, так как он используется в задачах"
        )
    
    try:
        db.delete(machine)
        db.commit()
        return {"message": "Станок успешно удален"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при удалении станка: {str(e)}"
        )
