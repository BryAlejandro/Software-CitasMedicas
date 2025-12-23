from app.repositories.repository import db

class GestionCitasService:
    @staticmethod
    def agendar_nueva_cita(cita):
        paciente = db.buscar_paciente_por_id(cita.paciente_id)
        if not paciente: return None, f"Error: El paciente con ID {cita.paciente_id} no existe."
        if len(cita.fecha) < 8: return None, "Error: El formato de fecha es incorrecto."
        return db.guardar_cita(cita), None

    @staticmethod
    def consultar_citas_externas(cedula: str):
        paciente = db.buscar_paciente_por_cedula(cedula)
        if not paciente: return None, "Paciente no encontrado."
        citas = db.buscar_citas_por_paciente(paciente["id"])
        return {
            "paciente": paciente["nombre"],
            "citas_atendidas": [c for c in citas if c["estado"] == "atendida"],
            "citas_canceladas": [c for c in citas if c["estado"] == "cancelada"],
            "citas_pendientes": [c for c in citas if c["estado"] == "pendiente"]
        }, None