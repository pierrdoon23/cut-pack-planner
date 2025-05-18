from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Roll, CuttingMap, Package, ChartPoint

db = SessionLocal()

# Добавим рулоны с разными типами нарезки, used/wasted и датами
rolls = [
    Roll(length=100.0, used=80.0, wasted=20.0, cutting_type="Уголки", created_at=datetime.utcnow() - timedelta(hours=2)),
    Roll(length=120.0, used=100.0, wasted=20.0, cutting_type="Ленты", created_at=datetime.utcnow() - timedelta(hours=3)),
    Roll(length=90.0, used=70.0, wasted=20.0, cutting_type="Уголки", created_at=datetime.utcnow() - timedelta(days=1, hours=1)),
    Roll(length=110.0, used=90.0, wasted=20.0, cutting_type="Ленты", created_at=datetime.utcnow() - timedelta(days=2)),
    Roll(length=130.0, used=110.0, wasted=20.0, cutting_type="Уголки", created_at=datetime.utcnow() - timedelta(days=3)),
]

# Добавим карты раскроя с разными датами
cutting_maps = [
    CuttingMap(created_at=datetime.utcnow() - timedelta(hours=1)),
    CuttingMap(created_at=datetime.utcnow() - timedelta(days=1)),
    CuttingMap(created_at=datetime.utcnow() - timedelta(days=2)),
]

# Добавим пакеты с разными датами
packages = [
    Package(created_at=datetime.utcnow() - timedelta(hours=1)),
    Package(created_at=datetime.utcnow() - timedelta(days=1)),
    Package(created_at=datetime.utcnow() - timedelta(days=2)),
]

# Добавим данные для барчарта
chart_points = [
    ChartPoint(label="Понедельник", value=5),
    ChartPoint(label="Вторник", value=8),
    ChartPoint(label="Среда", value=12),
    ChartPoint(label="Четверг", value=7),
    ChartPoint(label="Пятница", value=15),
    ChartPoint(label="Суббота", value=3),
    ChartPoint(label="Воскресенье", value=2),
]

db.add_all(rolls)
db.add_all(cutting_maps)
db.add_all(packages)
db.add_all(chart_points)
db.commit()
db.close()

print("Данные успешно добавлены!")