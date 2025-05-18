from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Stat(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    value = Column(Integer)
    change = Column(String)

class ChartPoint(Base):
    __tablename__ = "bar_chart"
    id = Column(Integer, primary_key=True)
    label = Column(String)
    value = Column(Integer)

class Roll(Base):
    __tablename__ = "rolls"
    id = Column(Integer, primary_key=True, index=True)
    length = Column(Float)

class CuttingMap(Base):
    __tablename__ = "cutting_maps"
    id = Column(Integer, primary_key=True, index=True)

class Package(Base):
    __tablename__ = "packages"
    id = Column(Integer, primary_key=True, index=True)
