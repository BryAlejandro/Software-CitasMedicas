import React, { useEffect, useState } from 'react';

function App() {
  const [pacientes, setPacientes] = useState([]);
  const [form, setForm] = useState({ cedula: '', nombre: '' });
  const [error, setError] = useState("");

  const refrescarLista = () => {
    fetch("http://127.0.0.1:8000/pacientes")
      .then(res => res.json())
      .then(data => setPacientes(data));
  };

  useEffect(() => { refrescarLista(); }, []);

  const validarYGuardar = (e) => {
    e.preventDefault();
    setError("");

    // VALIDACIÓN DE CÉDULA: Solo números y exactamente 10 dígitos (ajustar a 9 si prefieres)
    const regexCedula = /^[0-9]{10}$/; 
    if (!regexCedula.test(form.cedula)) {
      setError("La cédula debe tener exactamente 10 números.");
      return;
    }

    // VALIDACIÓN DE NOMBRE: Solo letras y espacios
    const regexNombre = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;
    if (!regexNombre.test(form.nombre)) {
      setError("El nombre solo debe contener letras.");
      return;
    }

    // Si pasa las validaciones, enviamos al backend
    fetch("http://127.0.0.1:8000/pacientes", {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ...form, apellido: "Registrado", especialidad: "General" })
    }).then(() => {
      refrescarLista();
      setForm({ cedula: '', nombre: '' });
    });
  };

  return (
    <div style={{ padding: '30px', fontFamily: 'Arial', maxWidth: '800px', margin: 'auto' }}>
      <h1>Gestión Médica UPS - Validada</h1>
      
      <div style={{ background: '#f4f7f6', padding: '20px', borderRadius: '8px', marginBottom: '20px' }}>
        <h3>Nuevo Registro</h3>
        <form onSubmit={validarYGuardar}>
          <input 
            placeholder="Cédula (10 dígitos)" 
            value={form.cedula} 
            maxLength={10}
            onChange={e => setForm({...form, cedula: e.target.value.replace(/\D/g, '')})} 
            style={{ padding: '8px', marginRight: '10px' }} required
          />
          <input 
            placeholder="Nombres y Apellidos" 
            value={form.nombre} 
            onChange={e => setForm({...form, nombre: e.target.value})} 
            style={{ padding: '8px', marginRight: '10px', width: '250px' }} required
          />
          <button type="submit" style={{ padding: '8px 15px', background: '#27ae60', color: 'white', border: 'none', cursor: 'pointer' }}>
            Guardar
          </button>
        </form>
        {error && <p style={{ color: 'red', fontWeight: 'bold', marginTop: '10px' }}>{error}</p>}
      </div>

      <table border="1" style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'center' }}>
        <thead style={{ background: '#34495e', color: 'white' }}>
          <tr><th>Cédula</th><th>Nombre</th><th>Acciones</th></tr>
        </thead>
        <tbody>
          {pacientes.map(p => (
            <tr key={p.cedula}>
              <td>{p.cedula}</td><td>{p.nombre}</td>
              <td>
                <button onClick={() => fetch(`http://127.0.0.1:8000/pacientes/${p.cedula}`, { method: 'DELETE' }).then(() => refrescarLista())}
                  style={{ background: '#e74c3c', color: 'white', border: 'none', padding: '5px', cursor: 'pointer' }}>
                  Eliminar
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;