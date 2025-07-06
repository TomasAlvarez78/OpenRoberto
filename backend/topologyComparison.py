import numpy as np
from neuralNetwork import NeuralNetwork
from neuralNetworkNoVector import NeuralNetworkNoVector
import time

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

ocultas = [2, 3, 5, 7, 10, 15, 20, 25, 30, 35, 40]
resultados = []

for h in ocultas:
    modelo = NeuralNetwork(input_size=4, hidden_size=h, output_size=2, learning_rate=0.1)
    start = time.time()
    modelo.train(X, Y, epochs=1000, print=False)
    end = time.time()

    salida = modelo.forward(X)
    mse = np.mean(np.square(Y - salida))
    resultados.append((h, mse, round((end - start)*1000, 2)))

print("\nComparativa de topologías:\n")
print("Ocultas | MSE       | Tiempo (ms)")
print("--------|-----------|-------------")
for h, mse, t in resultados:
    print(f"{h:^8} | {mse:.6f} | {t:^11}")
