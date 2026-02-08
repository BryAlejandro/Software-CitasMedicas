import React, { useEffect, useState } from 'react';

function App() {
  const [pacientes, setPacientes] = useState([]);
  const [status, setStatus] = useState("Conectando...");

  useEffect(() => {
    // 1. Verificar conexión inicial
    fetch("http://127.0.0.1:8000/")
      .then(res => res.json())
      .then(() => setStatus("Conectado ✅"))
      .catch(() => setStatus("Error de conexión ❌"));

    // 2. Cargar los pacientes reales del backend
    fetch("http://127.0.0.1:8000/pacientes")
      .then(res => res.json())
      .then(data => setPacientes(data))
      .catch(err => console.error("Error cargando pacientes:", err));
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'Segoe UI' }}>
      <h1 style={{ color: '#2c3e50' }}>Panel de Control - Citas Médicas</h1>
      <p>Estado del Servidor: <strong>{status}</strong></p>
      
      <hr />

      <h2>Listado de Pacientes (Desde Base de Datos)</h2>
      <table border="1" style={{ width: '100%', borderCollapse: 'collapse', marginTop: '10px' }}>
        <thead style={{ backgroundColor: '#f2f2f2' }}>
          <tr>
            <th>Cédula</th>
            <th>Nombre</th>
            <th>Apellido</th>
            <th>Especialidad Requerida</th>
          </tr>
        </thead>
        <tbody>
          {pacientes.length > 0 ? pacientes.map((p, index) => (
            <tr key={index}>
              <td>{p.cedula}</td>
              <td>{p.nombre}</td>
              <td>{p.apellido}</td>
              <td>{p.especialidad || 'General'}</td>
            </tr>
          )) : (
            <tr><td colSpan="4" style={{ textAlign: 'center' }}>No hay pacientes registrados.</td></tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default App;