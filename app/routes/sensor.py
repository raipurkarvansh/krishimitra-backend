# app/routes/sensor.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from app.database import get_db
from app.models.sensor_data import SensorData
from app.models.system_config import SystemConfig
from app.models.pump_log import PumpLog

router = APIRouter(tags=["Sensor"])


class SensorCreate(BaseModel):
    temperature: float
    humidity: float
    moisture: float
    pump_status: int   # ESP32 will send its current state (optional now)


@router.post("/sensor")
def create_sensor(data: SensorCreate, db: Session = Depends(get_db)):

    # 1️⃣ Save incoming sensor data
    new_data = SensorData(
        temperature=data.temperature,
        humidity=data.humidity,
        moisture=data.moisture,
        pump_status=data.pump_status
    )

    db.add(new_data)

    # 2️⃣ Get system config
    config = db.query(SystemConfig).first()

    # 3️⃣ AUTO Logic (Backend Controlled)
    if config and config.mode == "AUTO":

        LOWER_THRESHOLD = config.threshold
        UPPER_THRESHOLD = config.threshold + 10
        MIN_RUN_TIME = 30  # seconds

        # If Pump OFF → Check if should turn ON
        if config.pump_status == "OFF" and data.moisture < LOWER_THRESHOLD:

            config.pump_status = "ON"

            log = PumpLog(
                pump_status="ON",
                mode="AUTO",
                reason="LOW_MOISTURE"
            )
            db.add(log)

        # If Pump ON → Check if should turn OFF
        elif config.pump_status == "ON":

            last_on_log = db.query(PumpLog) \
                .filter(PumpLog.pump_status == "ON") \
                .order_by(PumpLog.timestamp.desc()) \
                .first()

            if last_on_log:
                run_time = (datetime.utcnow() - last_on_log.timestamp).total_seconds()
            else:
                run_time = 0

            if data.moisture > UPPER_THRESHOLD and run_time >= MIN_RUN_TIME:

                config.pump_status = "OFF"

                log = PumpLog(
                    pump_status="OFF",
                    mode="AUTO",
                    reason="MOISTURE_OK"
                )
                db.add(log)

    # 4️⃣ Commit all changes
    db.commit()
    db.refresh(new_data)

    # 5️⃣ Send BACKEND pump decision to ESP32
    config = db.query(SystemConfig).first()

    return {
        "id": new_data.id,
        "temperature": new_data.temperature,
        "humidity": new_data.humidity,
        "moisture": new_data.moisture,
        "pump_status": 1 if config and config.pump_status == "ON" else 0
    }
