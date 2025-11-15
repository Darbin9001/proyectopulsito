from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

from pydantic import BaseModel
from typing import Optional

# Define la base declarativa
Base = declarative_base()

# TODO: Crea tus modelos de datos aquí.
# Cada clase de modelo representa una tabla en tu base de datos.
# Debes renombrar YourModel por el nombre de la Clase según el servicio
class YourModel(Base):
    """
    Plantilla de modelo de datos para un recurso.
    Ajusta esta clase según los requisitos de tu tema.
    """
    __tablename__ = "[nombre_de_tu_tabla]"

    # Columnas de la tabla
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    # TODO: Agrega más columnas según sea necesario.
    # Por ejemplo:
    # is_active = Column(Boolean, default=True)
    # foreign_key_id = Column(Integer, ForeignKey("otra_tabla.id"))

    def __repr__(self):
        return f"<YourModel(id={self.id}, name='{self.name}')>"

# TODO: Define los modelos Pydantic para la validación de datos.
# Estos modelos se usarán en los endpoints de FastAPI para validar la entrada y salida.

class YourModelBase(BaseModel):
    name: str
    description: Optional[str] = None
    # TODO: Agrega los campos que se necesitan para crear o actualizar un recurso.

class YourModelCreate(YourModelBase):
    pass

class YourModelRead(YourModelBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True # Habilita la compatibilidad con ORM
