# Hacer

- interfaz gráfica -> tkinter ?
- API REST -> requests ?  | WebServer sino

# Pasos 

1. Inicializar pesos y bias - Ok
2. Definir tanh y su derivada - Ok
3. Implementar el forward pass - Ok
4. Implementar el algoritmo backpropagation - Ok
5. Entrenar la red - Ok
6. Probar con los mismos datos - ok
7. Agregar algo que veamos necesario

# Patrones con fallas

Siempre da KO: [1, -1, -1, 1] → Predicho: [[0.88 0.94]] → Redondeado: [1, 1]
Da KO 1 entre 5 veces: [-1, 1, 1, -1] → Predicho: [[-0.74 -0.92]] → Redondeado: [-1, -1]
Da OK 1 entre 5 veces: [-1, -1, 1, 1] → Predicho: [[-0.64  1.  ]] → Redondeado: [-1, 1]

# Commands

create app: npx create-react-app my-react-app

## front

install nvm: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash 
install node & npm: nvm install node
npm install
cd openrobertofront
npm start

## backend
source OpenRoberto/bin/activate
pip install -r requirements.txt
cd backend
uvicorn app:app

## Tiempos

V: 0.043193 s
NV: 0.563921 s

Hacer un script de metricas, extraer el promedio de tiempo entre V y NV para 1000 ejecuciones de la NN.
Sacar valores maximos en tiempo y valores minimos de cada uno para revisar margen de error

## Ports:

3000: Grafana
3001: FrontEnd
8000: Backend