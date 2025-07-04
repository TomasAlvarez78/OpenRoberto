import numpy as np
class NeuralNetwork:
    def __init__(self, input_size=4, hidden_size=5, output_size=2, learning_rate=0.1):
        self.W1 = np.random.uniform(-0.5, 0.5, (input_size, hidden_size))
        self.b1 = np.random.uniform(-0.5, 0.5, (1, hidden_size))
        self.W2 = np.random.uniform(-0.5, 0.5, (hidden_size, output_size))
        self.b2 = np.random.uniform(-0.5, 0.5, (1, output_size))
        self.learning_rate = learning_rate

    @staticmethod
    def tanh(x):
        return np.tanh(x)

    @staticmethod
    def tanh_derivative(x):
        return 1 - np.tanh(x) ** 2


    def forward(self, X):
        # Entrada → Capa oculta
        self.z1 = np.dot(X, self.W1) + self.b1
        self.a1 = self.tanh(self.z1)

        # Capa oculta → Capa de salida
        self.z2 = np.dot(self.a1, self.W2) + self.b2
        self.a2 = self.tanh(self.z2)

        return self.a2      
    
    def train_step(self, X, Y):
        output = self.forward(X)

        # print(output)

        # Error en la capa de salida
        error_output = output - Y
        delta_output = error_output * self.tanh_derivative(self.z2)

        # Error en la capa oculta
        error_hidden = np.dot(delta_output, self.W2.T)
        delta_hidden = error_hidden * self.tanh_derivative(self.z1)

        # Actualizar pesos y biaso
        self.W2 -= self.learning_rate * np.dot(self.a1.T, delta_output)
        self.b2 -= self.learning_rate * np.sum(delta_output, axis=0, keepdims=True)

        self.W1 -= self.learning_rate * np.dot(X.T, delta_hidden)
        self.b1 -= self.learning_rate * np.sum(delta_hidden, axis=0, keepdims=True)

        # Devuelve el error cuadrático medio para seguimiento
        return np.mean(np.square(error_output))
  
    def train(self, X, Y, epochs=1000, print_every=100, print = False):
        for epoch in range(epochs):
            loss = self.train_step(X, Y)
            if (epoch % print_every == 0) and print:
                print(f"Epoch {epoch}: Loss = {loss:.6f}")


    def summary(self):
        print("Red neuronal inicializada:")
        print(f"W2 shape: {self.W2}, b2 shape: {self.b2}")
        print(f"W1 shape: {self.W1}, b1 shape: {self.b1}")

        # print(f"W1 objeto {self.W1}")