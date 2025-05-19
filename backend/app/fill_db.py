from datetime import datetime, timedelta
import os
import sys
from sqlalchemy.orm import Session
# /backend python -m app.fill_db
# Добавляем путь для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
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
    db = SessionLocal()

    # Очистка всех таблиц
    db.query(TaskInfo).delete()
    db.query(Task).delete()
    db.query(Machine).delete()
    db.query(User).delete()
    db.query(TargetPackaging).delete()
    db.query(BaseMaterial).delete()
    db.commit()

    # Создаем базовые материалы
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

    # Создаем целевую упаковку
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

    # Создаем пользователей
    users = [
        User(
            full_name="Иванов Алексей Петрович",
            password="admin123",
            role=UserRole.ADMIN
        ),
        User(
            full_name="Петрова Мария Ивановна",
            password="manager123",
            role=UserRole.MANAGER
        ),
        User(
            full_name="Сидоров Олег Васильевич",
            password="operator123",
            role=UserRole.OPERATOR
        )
    ]

    # Создаем станки
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

    db.add_all(materials + target_packages + users + machines)
    db.commit()

    # Создаем задачи
    tasks = [
        Task(
            base_material_id=1,
            target_packaging_id=1,
            user_id=3
        ),
        Task(
            base_material_id=2,
            target_packaging_id=2,
            user_id=3
        )
    ]

    db.add_all(tasks)
    db.commit()

    # Создаем информацию о задачах
    now = datetime.utcnow()
    task_info = [
        TaskInfo(
            task_id=1,
            start_time=now - timedelta(hours=2),
            end_time=now - timedelta(hours=1),
            status=TaskStatus.COMPLETED,
            material_used=45.3,
            waste=2.7
        ),
        TaskInfo(
            task_id=2,
            start_time=now,
            status=TaskStatus.IN_PROGRESS,
            material_used=18.9,
            waste=0.5
        )
    ]

    db.add_all(task_info)
    db.commit()
    db.close()
    print("Тестовые данные успешно добавлены!")

if __name__ == "__main__":
    populate_test_data()