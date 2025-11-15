from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PacienteBase(BaseModel):
    cedula: str
    nombre: str
    apellido: str
    edad: Optional[int] = None
    telefono: Optional[str] = None

class PacienteCreate(PacienteBase):
    pass

class PacienteRead(PacienteBase):
    id: str
    fecha_registro: datetime
    
    class Config:
        from_attributes = True

class SignosVitalesBase(BaseModel):
    cedula_paciente: str  # Vincular con el paciente
    ritmo_cardiaco: int
    temperatura: float
    presion: str
    oxigeno: int

class SignosVitalesCreate(SignosVitalesBase):
    pass

class SignosVitalesRead(SignosVitalesBase):
    id: str
    timestamp: datetime
    nombre_paciente: Optional[str] = None
    
    class Config:
        from_attributes = True