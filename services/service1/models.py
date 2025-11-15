from pydantic import BaseModel
from datetime import datetime

class DatosVitales(BaseModel):
    timestamp: datetime
    frecuencia_cardiaca: int
    presion_sistolica: int
    presion_diastolica: int
    temperatura: float
    oxigeno: int
