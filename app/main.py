from app.routes import control
from app.database import SessionLocal
from app.models import SystemConfig
from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routes.users import router as users_router
from app.routes.sensor import router as sensor_router

app = FastAPI()

@app.on_event("startup")
def create_default_config():
    db = SessionLocal()
    config = db.query(SystemConfig).first()
    if not config:
        default = SystemConfig()
        db.add(default)
        db.commit()
    db.close()


Base.metadata.create_all(bind=engine)

app.include_router(users_router)
app.include_router(sensor_router)
app.include_router(control.router)


@app.get("/")
def root():
    return {"status": "Backend running"}

