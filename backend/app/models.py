from sqlalchemy import Column, Integer, String
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
