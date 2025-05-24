from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime
from backend.database.db import Base


class RawMeasurement(Base):
    __tablename__ = "raw_measurement"

    id = Column(Integer, primary_key=True, index=True)
    resource = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)


class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    resource = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    value = Column(Float, nullable=False)
    is_anomaly = Column(Boolean, nullable=False)
