import { useState } from 'react';

export default function RobotInterface() {
  const [sensors, setSensors] = useState({ S1: '', S2: '', S3: '', S4: '' });
  const [motors, setMotors] = useState({ M1: '', M2: '' });
  const [direccion, setDireccion] = useState('');
  const [respuestaAPI, setRespuestaAPI] = useState('');

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
      } else {
        setRespuestaAPI('Error en backend');
      }
    } catch (err) {
      setRespuestaAPI('Error de red');
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
      let responseText = data[0].Resp + " - " +  data[0].Desc
      if (data) {
        setRespuestaAPI(responseText || 'Respuesta recibida');
      } else {
        setRespuestaAPI('Respuesta vacía');
      }
    } catch (error) {
      setRespuestaAPI('Error en POST');
    }
  };

  const sensorLabels = {
    S1: 'Adelante',
    S2: 'Atrás',
    S3: 'Izquierda',
    S4: 'Derecha'
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-6 border rounded shadow-md">
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
          <span className="ml-2 text-sm text-gray-700">{respuestaAPI}</span>
        </div>
      </div>
    </div>
  );
}
