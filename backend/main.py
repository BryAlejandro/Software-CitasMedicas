from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware # IMPORTANTE
from app.models.models import Paciente, Cita
from app.repositories.repository import db
from app.services.service import GestionCitasService

app = FastAPI(title="Sistema Consultorio Médico - T02.03")

# --- CONFIGURACIÓN DE CORS (La llave que abre la puerta) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permite a tu React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NUEVA RUTA RAÍZ (Para que React no de error al cargar) ---
@app.get("/")
def read_root():
    return {"message": "Backend conectado con éxito", "proyecto": "UPS - Software Citas Médicas"}

# --- TUS RUTAS EXISTENTES ---
@app.get("/pacientes")
def get_pacientes(): 
    return db.buscar_todos_pacientes()

@app.post("/pacientes")
def post_paciente(paciente: Paciente): 
    return db.guardar_paciente(paciente)

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