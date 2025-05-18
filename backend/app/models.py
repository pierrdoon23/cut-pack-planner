from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base


class ChartPoint(Base):
    __tablename__ = "bar_chart"
    id = Column(Integer, primary_key=True)
    label = Column(String)
    value = Column(Integer)

class Roll(Base):
    __tablename__ = "rolls"
    id = Column(Integer, primary_key=True, index=True)
    length = Column(Float)
    used = Column(Float)
    wasted = Column(Float)
    cutting_type = Column(String)
    created_at = Column(DateTime)

class CuttingMap(Base):
    __tablename__ = "cutting_maps"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)

class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime)


