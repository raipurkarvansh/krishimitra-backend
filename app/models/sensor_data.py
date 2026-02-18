from sqlalchemy import Column, Integer, Float
from app.database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    temperature = Column(Float)
    humidity = Column(Float)
    moisture = Column(Float)
    pump_status = Column(Integer)
