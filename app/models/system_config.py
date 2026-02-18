from sqlalchemy import Column, Integer, String
from app.database import Base

class SystemConfig(Base):
    __tablename__ = "system_config"

    id = Column(Integer, primary_key=True, index=True)
    mode = Column(String(20), default="AUTO")          # 🔥 length added
    threshold = Column(Integer, default=3000)
    pump_status = Column(String(20), default="OFF")    # 🔥 length added
