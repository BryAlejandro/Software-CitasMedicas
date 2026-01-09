
# Tarea T02.03 - Construcción de aplicación de software
# Framework: FastAPI (Python)
# Arquitectura: Modelo / Repositorio / Servicio / Controlador

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn

app = FastAPI(
    title="Sistema de Gestión - Consultorio Médico",
    description="Backend desarrollado bajo estándares de Ingeniería de Software (Tarea T02.03)",
    version="1.0.0"
)

# --- CAPA 1: MODELO ---
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

# --- CAPA 2: REPOSITORIO ---
class ConsultorioRepository:
    def __init__(self):
        self._pacientes = [
            {"id": 1, "nombre": "Juan Perez", "cedula": "1712345678", "email": "jperez@mail.com", "telefono": "0999"},
            {"id": 2, "nombre": "Maria Lopez", "cedula": "0987654321", "email": "mlopez@mail.com", "telefono": "0888"}
        ]
        self._citas = []

    def buscar_todos_pacientes(self): return self._pacientes
    def guardar_paciente(self, paciente: Paciente):
        self._pacientes.append(paciente.model_dump())
        return paciente
    def buscar_paciente_por_id(self, paciente_id: int):
        return next((p for p in self._pacientes if p["id"] == paciente_id), None)
    def buscar_paciente_por_cedula(self, cedula: str):
        return next((p for p in self._pacientes if p["cedula"] == cedula), None)
    def guardar_cita(self, cita: Cita):
        if cita.id is None: cita.id = len(self._citas) + 1
        self._citas.append(cita.model_dump())
        return cita
    def buscar_citas_por_paciente(self, paciente_id: int):
        return [c for c in self._citas if c["paciente_id"] == paciente_id]

db = ConsultorioRepository()

# --- CAPA 3: SERVICIO ---
class GestionCitasService:
    @staticmethod
    def agendar_nueva_cita(cita: Cita):
        paciente = db.buscar_paciente_por_id(cita.paciente_id)
        if not paciente: return None, f"Error: El paciente con ID {cita.paciente_id} no existe."
        if len(cita.fecha) < 8: return None, "Error: El formato de fecha es incorrecto."
        nueva_cita = db.guardar_cita(cita)
        return nueva_cita, None

    @staticmethod
    def consultar_citas_externas(cedula: str):
        paciente = db.buscar_paciente_por_cedula(cedula)
        if not paciente: return None, "Paciente no encontrado."
        citas = db.buscar_citas_por_paciente(paciente["id"])
        resultado = {
            "paciente": paciente["nombre"],
            "citas_atendidas": [c for c in citas if c["estado"] == "atendida"],
            "citas_canceladas": [c for c in citas if c["estado"] == "cancelada"],
            "citas_pendientes": [c for c in citas if c["estado"] == "pendiente"]
        }
        return resultado, None

# --- CAPA 4: CONTROLADOR ---
@app.get("/pacientes", tags=["Gestión de Pacientes"])
def get_pacientes(): return db.buscar_todos_pacientes()

@app.post("/pacientes", tags=["Gestión de Pacientes"])
def post_paciente(paciente: Paciente): return db.guardar_paciente(paciente)

@app.post("/citas", tags=["Gestión de Citas"], response_model=Cita)
def post_cita(cita: Cita):
    resultado, error = GestionCitasService.agendar_nueva_cita(cita)
    if error: raise HTTPException(status_code=400, detail=error)
    return resultado

@app.get("/api/citas/consulta", tags=["Servicios Externos"])
def consultar_citas_paciente(cedula: str = Query(..., description="Cédula del paciente")):
    resultado, error = GestionCitasService.consultar_citas_externas(cedula)
    if error: raise HTTPException(status_code=404, detail=error)
    return resultado
