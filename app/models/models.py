from pydantic import BaseModel
from typing import Optional

class Paciente(BaseModel):
    id: int
    nombre: str
    cedula: str
    email: str
    telefono: str

class Cita(BaseModel):
    id: Optional[int] = None 
    paciente_id: int
    medico: str
    fecha: str
    motivo: str
    observaciones: str
    estado: str = "pendiente"