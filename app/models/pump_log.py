from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class PumpLog(Base):
    __tablename__ = "pump_log"

    id = Column(Integer, primary_key=True, index=True)
    pump_status = Column(String(20))
    mode = Column(String(20))
    reason = Column(String(50))
    timestamp = Column(DateTime, default=datetime.utcnow)
