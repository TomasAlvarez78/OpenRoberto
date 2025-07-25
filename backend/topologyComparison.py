import numpy as np
from neuralNetwork import NeuralNetwork
from neuralNetworkNoVector import NeuralNetworkNoVector
import time
import csv

# Patrones de entrenamiento
pattern = [
    [1, 1, 1, 1, -1, -1],
    [-1, 1, 1, 1, -1, 1],
    [1, 1, -1, -1, 1, -1],
    [-1, -1, -1, -1, 1, 1],
    [1, -1, 1, 1, 1, -1],
    [1, 1, -1, 1, -1, 1],
    [1, 1, 1, -1, 1, -1]
]

X = np.array([row[:4] for row in pattern])
Y = np.array([row[4:] for row in pattern])

ocultas = [2, 3, 5, 7, 10, 20]
for modo, Clase in {'Vectorizado': NeuralNetwork, 'NoVectorizado': NeuralNetworkNoVector}.items():
    resultados = []
    for h in ocultas:
        modelo = Clase(input_size=4, hidden_size=h, output_size=2, learning_rate=0.1)
        start = time.time()
        modelo.train(X, Y, epochs=1000, print=False)
        end = time.time()

        salida = modelo.forward(X)
        mse = np.mean(np.square(Y - salida))
        resultados.append((h, round(mse, 7), round((end - start)*1000, 2)))

    # Guardar en CSV
    fileName = f"resultados_topologia_{modo}.csv"
    with open(fileName, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["neuronas_ocultas", "error_mse", "tiempo_ms"])
        for fila in resultados:
            writer.writerow(fila)

    print(f"\nComparativa de topologías {modo}\n")
    print("Ocultas | MSE         | Tiempo (ms)")
    print("--------|-------------|-------------")
    for h, mse, t in resultados:
        print(f"{h:^8} | {mse:.7f} | {t:^11}")



