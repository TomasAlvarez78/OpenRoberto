import { useState, useEffect } from 'react';

export default function RobotInterface() {
  const [sensors, setSensors] = useState({ S1: '', S2: '', S3: '', S4: '' });
  const [motors, setMotors] = useState({ M1: '', M2: '' });
  const [direccion, setDireccion] = useState('');
  const [respuestaAPI, setRespuestaAPI] = useState('');
  const [tiempo, setTiempo] = useState('');
  const [tiempoResult, setTiempoResult] = useState('');
  const [modelo, setModelo] = useState('Vectorizado');

  useEffect(() => {
    fetchTiempo();
  }, [modelo]);

  const fetchTiempo = async () => {
    const res = await fetch("http://localhost:8000/tiempo-entrenamiento");
    const data = await res.json();
    setTiempo(`${data.modelo} → ${data.tiempo_ms} ms`);
  };

  const toggleModelo = async () => {
    const nuevoModelo = modelo === 'Vectorizado' ? 'NoVectorizado' : 'Vectorizado';
    setModelo(nuevoModelo);
    await fetch("http://localhost:8000/set-modelo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ modelo: nuevoModelo }),
    });
    fetchTiempo();
  };

  const getRobotOrientation = () => {
    if (direccion === 'Avanzar') return '⬆️';
    if (direccion === 'Retroceder') return '⬇️';
    if (direccion === 'Girar Izquierda') return '⬅️';
    if (direccion === 'Girar Derecha') return '➡️';
    return '🤖';
  };

  const setDireccionFromOutput = ([m1, m2]) => {
    if (m1 === 1 && m2 === 1) setDireccion("Avanzar");
    else if (m1 === -1 && m2 === -1) setDireccion("Retroceder");
    else if (m1 === 1 && m2 === -1) setDireccion("Girar Derecha");
    else if (m1 === -1 && m2 === 1) setDireccion("Girar Izquierda");
    else setDireccion("Desconocida");
  };

  const handleGetAPI = async () => {
    try {
      const res = await fetch("http://localhost:8000/predict");
      const data = await res.json();

      if (data.sensores) {
        setSensors({
          S1: data.sensores.S1,
          S2: data.sensores.S2,
          S3: data.sensores.S3,
          S4: data.sensores.S4
        });

        setMotors({
          M1: data.sensores.M1,
          M2: data.sensores.M2
        });

        setDireccionFromOutput([parseInt(data.sensores.M1), parseInt(data.sensores.M2)]);
        setTiempoResult(`${data.tiempos_entrenamientoResult} ms`);
      } else {
        setRespuestaAPI('KO - Error en backend');
      }
    } catch (err) {
      setRespuestaAPI('KO - Error de red');
    }
  };

  const handlePostAPI = async () => {
    const resultado = {
      S1: sensors.S1,
      S2: sensors.S2,
      S3: sensors.S3,
      S4: sensors.S4,
      M1: motors.M1,
      M2: motors.M2,
    };

    try {
      const response = await fetch("http://localhost:8000/verify", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify([resultado]),
      });

      const data = await response.json();
      let responseText = data[0].Resp + (data[0].Desc ? " - " + data[0].Desc : "");
      if (data) {
        setRespuestaAPI(responseText || 'OK - Respuesta recibida');
      } else {
        setRespuestaAPI('KO - Respuesta vacía');
      }
    } catch (error) {
      setRespuestaAPI('KO - Error en POST');
    }
  };

  const handleGenerarCSV = async () => {
    const res = await fetch("http://localhost:8000/generar-csv");
    const data = await res.json();
    alert(data.mensaje);
  };

  const sensorLabels = {
    S1: 'Adelante',
    S2: 'Atrás',
    S3: 'Izquierda',
    S4: 'Derecha'
  };

  return (
    <div className="flex flex-col lg:flex-row gap-6 max-w-7xl mx-auto mt-10 p-4">
      <div className="w-full lg:w-1/2 p-6 border rounded shadow-md">
        <div className="space-y-4">
          <h2 className="text-lg font-semibold text-center">Sensores</h2>
          <div className="grid grid-cols-4 gap-2">
            {['S1', 'S2', 'S3', 'S4'].map((s) => (
              <div key={s} className="flex flex-col items-center">
                <span className="text-sm text-gray-600">{sensorLabels[s]}</span>
                <input
                  name={s}
                  value={sensors[s]}
                  readOnly
                  placeholder={s}
                  className={`border p-2 rounded text-center w-20 font-bold ${sensors[s] === '-1' ? 'bg-green-200 text-green-800' : sensors[s] === '1' ? 'bg-red-200 text-red-800' : 'bg-gray-100'}`}
                />
              </div>
            ))}
          </div>

          <div className="grid grid-cols-3 gap-2 items-center">
            <input
              name="M1"
              value={motors.M1}
              readOnly
              placeholder="M1"
              className="border p-2 rounded bg-gray-100"
            />
            <input
              name="M2"
              value={motors.M2}
              readOnly
              placeholder="M2"
              className="border p-2 rounded bg-gray-100"
            />
            <input
              name="direccion"
              value={direccion}
              readOnly
              placeholder="Dirección"
              className="border p-2 rounded col-span-1 bg-gray-100"
            />
          </div>

          <div className="text-center text-3xl">
            {getRobotOrientation()}
          </div>

          <div className="flex justify-center gap-4 pt-4 items-center">
            <button
              onClick={handleGetAPI}
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
            >
              Consulta Get - API
            </button>
            <button
              onClick={handlePostAPI}
              className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
            >
              Consulta Post - API
            </button>
          </div>

          {/* Mensaje respuestaAPI mejorado y centrado */}
          <div className="flex justify-center pt-4">
            {respuestaAPI && (
              <div
                className={`inline-flex items-center gap-2 px-4 py-2 rounded-lg font-semibold
                  ${
                    respuestaAPI.startsWith('OK')
                      ? 'bg-green-100 text-green-800'
                      : respuestaAPI.startsWith('KO')
                      ? 'bg-red-100 text-red-800'
                      : 'bg-gray-100 text-gray-700'
                  }
                `}
                role="alert"
                aria-live="polite"
              >
                {respuestaAPI.startsWith('OK') && (
                  <span aria-hidden="true" className="text-xl">✅</span>
                )}
                {respuestaAPI.startsWith('KO') && (
                  <span aria-hidden="true" className="text-xl">❌</span>
                )}
                <span>{respuestaAPI}</span>
              </div>
            )}
          </div>

          {/* Mejora visual para tiempos con animación y diseño */}
          <div className="flex justify-center gap-8 mt-6">
            <div className="bg-blue-100 text-blue-800 px-6 py-4 rounded-lg shadow-md flex items-center gap-3 min-w-[240px] animate-fadeIn">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 8v4l3 3m6 0a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <div className="text-sm font-semibold tracking-wide">Tiempo de Entrenamiento</div>
                <div className="text-2xl font-extrabold">{tiempo || '--'}</div>
              </div>
            </div>

            <div className="bg-green-100 text-green-800 px-6 py-4 rounded-lg shadow-md flex items-center gap-3 min-w-[240px] animate-fadeIn">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-7 w-7 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-3-3v6m7-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <div className="text-sm font-semibold tracking-wide">Tiempo de Procesado</div>
                <div className="text-2xl font-extrabold">{tiempoResult || '--'}</div>
              </div>
            </div>
          </div>

          <div className="text-center pt-4">
            <button
              onClick={toggleModelo}
              className="bg-purple-500 text-white px-4 py-1 rounded hover:bg-purple-600"
            >
              Cambiar a: {modelo === 'Vectorizado' ? 'NoVectorizado' : 'Vectorizado'}
            </button>
          </div>
          <div className="text-center pt-2">
            <button
              onClick={handleGenerarCSV}
              className="bg-green-500 text-white px-4 py-1 rounded hover:bg-green-600"
            >
              Generar CSV Topologías
            </button>
          </div>
        </div>
      </div>

      <div className="w-full lg:w-1/2 p-6 border rounded shadow-md">
        <h2 className="text-lg font-semibold text-center mb-4">Visualización en Grafana</h2>
        <div className="space-y-4 flex flex-col items-center">
          <iframe
            src="http://localhost:3000/d-solo/9a4c4172-0615-447f-8d27-4007cc084d84/error-cuadratico-medio-por-neurona?orgId=1&from=1751825666771&to=1751847266771&timezone=browser&panelId=1&__feature.dashboardSceneSolo"
            width="450"
            height="200"
            frameBorder="0"
            className="rounded border"
            title="Error Cuadrático Medio - V"
          ></iframe>
          <iframe
            src="http://localhost:3000/d-solo/9a4c4172-0615-447f-8d27-4007cc084d84/error-cuadratico-medio-por-neurona?orgId=1&from=1751825763693&to=1751847363693&timezone=browser&panelId=2&__feature.dashboardSceneSolo"
            width="450"
            height="200"
            frameBorder="0"
            className="rounded border"
            title="Error Cuadrático Medio - NV"
          ></iframe>
        </div>
      </div>

      <style jsx>{`
        @keyframes fadeIn {
          from {opacity: 0; transform: translateY(10px);}
          to {opacity: 1; transform: translateY(0);}
        }
        .animate-fadeIn {
          animation: fadeIn 0.5s ease forwards;
        }
      `}</style>
    </div>
  );
}
