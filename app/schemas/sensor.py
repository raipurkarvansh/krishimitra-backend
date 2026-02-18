from pydantic import BaseModel


class SensorCreate(BaseModel):
    temperature: float
    moisture: float


class SensorResponse(BaseModel):
    id: int
    temperature: float
    moisture: float

    class Config:
        orm_mode = True
