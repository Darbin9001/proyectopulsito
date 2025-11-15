from pydantic import BaseModel
from typing import Optional

# Plantilla para modelos Pydantic (útil para validación de datos en endpoints)
class ExampleModel(BaseModel):
    name: str
    description: Optional[str] = None
    # Agrega aquí los campos que necesites para tu microservicio

# Si en el futuro necesitas modelos SQL, puedes usar SQLAlchemy (ver documentación oficial)
