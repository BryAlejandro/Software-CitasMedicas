from app.models.models import Paciente, Cita

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

# Singleton para persistencia en memoria durante la ejecución
db = ConsultorioRepository()