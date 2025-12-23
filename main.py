from fastapi import FastAPI, HTTPException, Query
from app.models.models import Paciente, Cita
from app.repositories.repository import db
from app.services.service import GestionCitasService

app = FastAPI(title="Sistema Consultorio Médico - T02.03")

@app.get("/pacientes")
def get_pacientes(): return db.buscar_todos_pacientes()

@app.post("/pacientes")
def post_paciente(paciente: Paciente): return db.guardar_paciente(paciente)

@app.post("/citas", response_model=Cita)
def post_cita(cita: Cita):
    res, err = GestionCitasService.agendar_nueva_cita(cita)
    if err: raise HTTPException(status_code=400, detail=err)
    return res

@app.get("/api/citas/consulta")
def consultar(cedula: str):
    res, err = GestionCitasService.consultar_citas_externas(cedula)
    if err: raise HTTPException(status_code=404, detail=err)
    return res