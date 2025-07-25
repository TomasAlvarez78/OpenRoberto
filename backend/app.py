import numpy as np
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from neuralNetwork import NeuralNetwork
from neuralNetworkNoVector import NeuralNetworkNoVector
from client import Client
import time
import subprocess
import csv

# Generacion de datos inversos

# def generar_combinaciones_binarias():
#     return [list(p) for p in product([1, -1], repeat=4)]

# def obtener_patrones_no_entrenados(todos, entrenados):
#     entrenados_set = {tuple(p[:4]) for p in entrenados}
#     return [p for p in todos if tuple(p) not in entrenados_set]

modelo_actual = 'Vectorizado'
modelos = {}
tiempos_entrenamiento = {}

def entrenar_modelos():
    global modelos, tiempos_entrenamiento

    modelos = {}
    tiempos_entrenamiento = {}

    for modo, Clase in {'Vectorizado': NeuralNetwork, 'NoVectorizado': NeuralNetworkNoVector}.items():
        modelo = Clase()
        start = time.perf_counter()
        modelo.train(X, Y, epochs=1000, print_every=100, print=False)
        end = time.perf_counter()

        modelos[modo] = modelo
        tiempos_entrenamiento[modo] = round((end - start) * 1000, 2)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Client

client = Client("https://www.agurait.com/ubp/sia/2022/roberto/")

# Red Neuronal

pattern = [
    # S1 S2 S3 S4   M1 M2
    [ 1, 1, 1, 1,  -1, -1],  # Rodeado → retroceder
    [-1, 1, 1, 1,  -1,  1],  # Gira hacia la izquierda
    [ 1, 1,-1,-1,   1, -1],  # Gira hacia la derecha
    [-1,-1,-1,-1,   1,  1],  # Todo libre → avanzar
    [ 1,-1, 1, 1,   1, -1],  # Gira hacia la derecha
    [ 1, 1,-1, 1,  -1,  1],  # Gira hacia la izquierda
    [ 1, 1, 1,-1,   1, -1],  # Gira hacia la derecha
]


X = np.array([row[:4] for row in pattern]) # Entrada
Y = np.array([row[4:] for row in pattern]) # Salida

entrenar_modelos()
nn = modelos[modelo_actual]

# Fin Red Neuronal

# Endpoints

@app.get("/predict")
def predict():
    sensores = client.get()
    
    print(f"API Get Response: {sensores}")
    
    entrada = np.array([[int(sensores['S1']), int(sensores['S2']), int(sensores['S3']), int(sensores['S4'])]])
    
    startResult = time.perf_counter()
    salida = np.where(nn.forward(entrada) >= 0, 1, -1).tolist()[0]
    endResult = time.perf_counter()
    tiempos_entrenamientoResult = round((endResult - startResult) * 1000, 2)    

    sensores_con_motores = {
        **sensores,
        "M1": str(salida[0]),
        "M2": str(salida[1]),
    }

    return { "sensores": sensores_con_motores, "tiempos_entrenamientoResult": tiempos_entrenamientoResult }

@app.post("/verify")
async def verify(request: Request):
    data = await request.json()
    resultado = data[0]

    respuesta = client.post(resultado)

    print(f"API POST Response: {respuesta}")
    
    return respuesta

@app.post("/set-modelo")
async def set_modelo(request: Request):
    global modelo_actual, nn
    body = await request.json()
    nuevo_modelo = body.get("modelo")

    if nuevo_modelo not in modelos:
        return {"error": "Modelo inválido"}

    modelo_actual = nuevo_modelo
    nn = modelos[modelo_actual]
    return {"modelo": modelo_actual}

@app.get("/tiempo-entrenamiento")
def tiempo_entrenamiento():
    return {
        "modelo": modelo_actual,
        "tiempo_ms": tiempos_entrenamiento.get(modelo_actual, "No disponible")
    }


@app.get("/generar-csv")
def generar_csv():
    try:
        salida = subprocess.run(
            ["python3", "topologyComparison.py"], capture_output=True, text=True
        )
        if salida.returncode == 0:
            return {"status": "ok", "mensaje": "CSV generado correctamente"}
        else:
            return {"status": "error", "mensaje": salida.stderr}
    except Exception as e:
        return {"status": "error", "mensaje": str(e)}
    
@app.get("/resultados-csv")
def resultados_csv():
    base_path = "./"
    archivos = {
        "vectorizado": f"{base_path}/resultados_topologia_Vectorizado.csv",
        "no_vectorizado": f"{base_path}/resultados_topologia_NoVectorizado.csv"
    }

    resultados = {}
    for clave, archivo in archivos.items():
        try:
            with open(archivo, newline='') as f:
                reader = csv.DictReader(f)
                resultados[clave] = [row for row in reader]
        except FileNotFoundError:
            resultados[clave] = f"Archivo no encontrado: {archivo}"

    return JSONResponse(content=resultados)
    
# Fin Endpoints
    

