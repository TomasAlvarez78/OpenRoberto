import numpy as np
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from neuralNetwork import NeuralNetwork
from neuralNetworkNoVector import NeuralNetworkNoVector
from client import Client
import time

# from itertools import product

# def generar_combinaciones_binarias():
#     return [list(p) for p in product([1, -1], repeat=4)]

# def obtener_patrones_no_entrenados(todos, entrenados):
#     entrenados_set = {tuple(p[:4]) for p in entrenados}
#     return [p for p in todos if tuple(p) not in entrenados_set]

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
    [-1, 1, 1, 1,   -1,  1], # Gira hacia la izquierda
    [ 1, 1,-1,-1,   1, -1],  # Gira hacia la derecha
    [-1,-1,-1,-1,   1,  1],  # Todo libre → avanzar
    [ 1,-1, 1, 1,   1, -1],  # Gira hacia la derecha
    [ 1, 1,-1, 1,  -1,  1],  # Gira hacia la izquierda
    [ 1, 1, 1,-1,   1, -1],  # Gira hacia la derecha
]

X = np.array([row[:4] for row in pattern]) # Entrada
Y = np.array([row[4:] for row in pattern]) # Salida

nn = NeuralNetwork()
# nn = NeuralNetworkNoVector()
print("Inicializacion entramiento")
inicio = time.perf_counter()
nn.train(X, Y, epochs=1000, print_every=100, print=False)
fin = time.perf_counter()
print("Finalizacion entramiento")
tiempo_transcurrido = fin - inicio
print(f"Tiempo transcurrido: {tiempo_transcurrido:.6f} segundos")

# Fin Red Neuronal

# print("\n Evaluación de patrones NO vistos durante el entrenamiento \n")
# for entrada in patrones_no_entrenados:
#     entrada_np = np.array(entrada).reshape(1, -1)
#     salida_pred = nn.forward(entrada_np)
#     salida_redondeada = np.where(salida_pred >= 0, 1, -1)

#     print(f"Entrada: {entrada} → Predicho: {np.round(salida_pred, 2)} → Redondeado: {salida_redondeada.tolist()[0]}")

# print("\n Pruebas de la red entrenada ")
# for i, entrada in enumerate(X):
    # salida_real = Y[i]
    # salida_predicha = nn.forward(entrada.reshape(1, -1))
    # salida_predicha_redondeada = np.round(salida_predicha, 2)
    # print(f"Entrada: {entrada} → Esperado: {salida_real} | Predicho: {salida_predicha_redondeada}")

# profe = [-1,-1,-1,1]
# profe_salida_predicha = nn.forward(profe)
# profe_salida_predicha_redondeada = np.round(profe_salida_predicha, 2)
# print(f"Valor predicho: {np.round(profe_salida_predicha, 2)}")

# print("Salida:", salida)
# nn.summary()

# Cliente ---------------------------------------------

# estado = client.get()
# print("Estado actual:", estado)

# entrada = client.JSONtoArray(estado)
# profe_salida_predicha = nn.forward(entrada)
# print(f"Valor predicho: {np.round(profe_salida_predicha, 2)}")

# ---------------------------------------------

@app.get("/predict")
def predict():
    sensores = client.get()
    
    print(f"API Get Response: {sensores}")
    
    entrada = np.array([[int(sensores['S1']), int(sensores['S2']), int(sensores['S3']), int(sensores['S4'])]])
    
    salida = np.where(nn.forward(entrada) >= 0, 1, -1).tolist()[0]

    sensores_con_motores = {
        **sensores,
        "M1": str(salida[0]),
        "M2": str(salida[1]),
    }

    return { "sensores": sensores_con_motores }

@app.post("/verify")
async def verify(request: Request):
    data = await request.json()
    resultado = data[0]

    respuesta = client.post(resultado)

    print(f"API POST Response: {respuesta}")
    
    return respuesta
    
