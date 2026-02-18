# app/routes/control.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.system_config import SystemConfig
from app.models.pump_log import PumpLog

router = APIRouter(prefix="/control", tags=["Control"])


# ---------------------------
# MODE CONTROL
# ---------------------------

@router.post("/mode/auto")
def set_auto(db: Session = Depends(get_db)):
    config = db.query(SystemConfig).first()
    config.mode = "AUTO"
    db.commit()
    return {"mode": "AUTO"}


@router.post("/mode/manual")
def set_manual(db: Session = Depends(get_db)):
    config = db.query(SystemConfig).first()
    config.mode = "MANUAL"
    db.commit()
    return {"mode": "MANUAL"}


# ---------------------------
# MANUAL PUMP CONTROL (WITH LOGGING)
# ---------------------------

@router.post("/pump/on")
def pump_on(db: Session = Depends(get_db)):
    config = db.query(SystemConfig).first()

    # Avoid duplicate logs
    if config.pump_status != "ON":
        config.pump_status = "ON"

        log = PumpLog(
            pump_status="ON",
            mode="MANUAL",
            reason="MANUAL_OVERRIDE"
        )
        db.add(log)

        db.commit()

    return {"pump_status": "ON"}


@router.post("/pump/off")
def pump_off(db: Session = Depends(get_db)):
    config = db.query(SystemConfig).first()

    # Avoid duplicate logs
    if config.pump_status != "OFF":
        config.pump_status = "OFF"

        log = PumpLog(
            pump_status="OFF",
            mode="MANUAL",
            reason="MANUAL_OVERRIDE"
        )
        db.add(log)

        db.commit()

    return {"pump_status": "OFF"}


# ---------------------------
# THRESHOLD CONTROL
# ---------------------------

@router.post("/threshold/{value}")
def set_threshold(value: int, db: Session = Depends(get_db)):
    config = db.query(SystemConfig).first()
    config.threshold = value
    db.commit()
    return {"threshold": value}


# ---------------------------
# FETCH PUMP LOG HISTORY
# ---------------------------

@router.get("/pump/logs")
def get_logs(db: Session = Depends(get_db)):
    return db.query(PumpLog).order_by(PumpLog.timestamp.desc()).all()
