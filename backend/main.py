from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.repositories.repository import db # Importa tu base de datos simulada

app = FastAPI(title="Sistema Médico UPS - Versión Final")

# Configuración de CORS: Permite que React (puerto 3000) hable con FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Servidor activo", "proyecto": "Citas Médicas UPS"}

@app.get("/pacientes")
def get_pacientes():
    # Retorna la lista de pacientes actual
    return db.buscar_todos_pacientes()

@app.post("/pacientes")
def post_paciente(paciente: dict):
    # Solución al error model_dump: Guardamos el diccionario directamente en la lista
    try:
        db._pacientes.append(paciente)
        return {"message": "Paciente registrado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/pacientes/{cedula}")
def eliminar_paciente(cedula: str):
    # Solución al AttributeError: Acceso por llave ['cedula']
    for i, p in enumerate(db._pacientes):
        if p["cedula"] == cedula:
            db._pacientes.pop(i)
            return {"message": "Paciente eliminado"}
    
    raise HTTPException(status_code=404, detail="Paciente no encontrado")