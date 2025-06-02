# /backend python -m app.fill_db
from datetime import datetime, timedelta
import os
import sys
from decimal import Decimal
from sqlalchemy.orm import Session

# Добавляем путь для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, Base, engine
from app.models import (
    BaseMaterial,
    TargetPackaging,
    User,
    Machine,
    Task,
    TaskInfo,
    UserRole,
    TaskStatus,
    PackagingType,
    SeamType
)

def populate_test_data():
    # Создаем все таблицы
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    # Очистка всех таблиц
    db.query(TaskInfo).delete()
    db.query(Task).delete()
    db.query(Machine).delete()
    db.query(User).delete()
    db.query(TargetPackaging).delete()
    db.query(BaseMaterial).delete()
    db.commit()

    # 1. Базовые материалы
    materials = [
        BaseMaterial(
            name="Пленка вакуумная 100мкм",
            length=200.0,
            width=1.5,
            thickness=100.0,
            package_type=PackagingType.VACUUM
        ),
        BaseMaterial(
            name="Пленка флоу-пак 80мкм",
            length=150.0,
            width=1.2,
            thickness=80.0,
            package_type=PackagingType.FLOW_PACK
        ),
        BaseMaterial(
            name="Пленка термоусадочная 120мкм",
            length=180.0,
            width=1.8,
            thickness=120.0,
            package_type=PackagingType.SHRINK
        )
    ]
    db.add_all(materials)
    db.commit()

    # 2. Целевая упаковка
    target_packages = [
        TargetPackaging(
            name="Упаковка для сосисок",
            purpose="Упаковка сосисок премиум класса",
            length=0.3,
            width=0.2,
            package_type=PackagingType.VACUUM,
            seam_type=SeamType.DOUBLE_SEAM,
            is_two_streams=True
        ),
        TargetPackaging(
            name="Упаковка для колбас",
            purpose="Упаковка сырокопченых колбас",
            length=0.5,
            width=0.3,
            package_type=PackagingType.FLOW_PACK,
            seam_type=SeamType.ULTRASONIC,
            is_two_streams=False
        )
    ]
    db.add_all(target_packages)
    db.commit()

    # 3. Пользователи
    users = [
        User(
            full_name="Иванов Алексей Петрович",
            password="admin123",
            role=UserRole.ADMIN
        ),
        User(
            full_name="Сидоров Олег Васильевич",
            password="operator123",
            role=UserRole.OPERATOR
        )
    ]
    db.add_all(users)
    db.commit()

    # 4. Станки
    machines = [
        Machine(
            name="Резчик VECTOR-3000",
            cutting_speed=15.5,
            machine_width=2.0
        ),
        Machine(
            name="Автомат FPM-200",
            cutting_speed=20.0,
            machine_width=1.8
        )
    ]
    db.add_all(machines)
    db.commit()

    # 5. Задачи
    now = datetime.utcnow()
    tasks = [
        Task(
            base_material_id=materials[0].id,
            target_packaging_id=target_packages[0].id,
            user_id=users[0].id,
            machine_id=machines[0].id,
            status=TaskStatus.COMPLETED,
            start_time=now - timedelta(hours=3)
        ),
        Task(
            base_material_id=materials[1].id,
            target_packaging_id=target_packages[1].id,
            user_id=users[1].id,
            machine_id=machines[1].id,
            status=TaskStatus.IN_PROGRESS,
            start_time=now
        )
    ]
    db.add_all(tasks)
    db.commit()

    # 6. Информация о задачах
    task_info = [
        TaskInfo(
            task_id=tasks[0].id,
            start_time=tasks[0].start_time,
            end_time=now,
            status=TaskStatus.COMPLETED,
            value=1000,
            material_used=Decimal("45.30"),
            waste=Decimal("2.70")
        ),
        TaskInfo(
            task_id=tasks[1].id,
            start_time=tasks[1].start_time,
            end_time=now + timedelta(hours=4),
            status=TaskStatus.IN_PROGRESS,
            value=500,
            material_used=Decimal("18.90"),
            waste=Decimal("0.50")
        )
    ]
    db.add_all(task_info)
    db.commit()

    db.close()
    print("Тестовые данные успешно добавлены!")

if __name__ == "__main__":
    populate_test_data()
