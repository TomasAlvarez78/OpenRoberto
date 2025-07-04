import numpy as np

class NeuralNetworkNoVector:
    def __init__(self, input_size=4, hidden_size=5, output_size=2, learning_rate=0.1):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.learning_rate = learning_rate

        self.W1 = np.random.uniform(-0.5, 0.5, (input_size, hidden_size))
        self.b1 = np.random.uniform(-0.5, 0.5, (1, hidden_size))
        self.W2 = np.random.uniform(-0.5, 0.5, (hidden_size, output_size))
        self.b2 = np.random.uniform(-0.5, 0.5, (1, output_size))

    def tanh(self, x):
        return np.tanh(x)

    def tanh_derivative(self, x):
        return 1 - np.tanh(x) ** 2

    def forward(self, X):
        batch_size = X.shape[0]
        self.z1 = np.zeros((batch_size, self.hidden_size))
        self.a1 = np.zeros((batch_size, self.hidden_size))
        self.z2 = np.zeros((batch_size, self.output_size))
        self.a2 = np.zeros((batch_size, self.output_size))

        for n in range(batch_size):
            for j in range(self.hidden_size):
                suma = sum(X[n][i] * self.W1[i][j] for i in range(self.input_size)) + self.b1[0][j]
                self.z1[n][j] = suma
                self.a1[n][j] = self.tanh(suma)

            for k in range(self.output_size):
                suma = sum(self.a1[n][j] * self.W2[j][k] for j in range(self.hidden_size)) + self.b2[0][k]
                self.z2[n][k] = suma
                self.a2[n][k] = self.tanh(suma)

        return self.a2

    def train_step(self, X, Y):
        output = self.forward(X)

        error_output = output - Y
        delta_output = error_output * self.tanh_derivative(self.z2)

        error_hidden = np.zeros((X.shape[0], self.hidden_size))
        delta_hidden = np.zeros((X.shape[0], self.hidden_size))

        for n in range(X.shape[0]):
            for j in range(self.hidden_size):
                error_hidden[n][j] = sum(delta_output[n][k] * self.W2[j][k] for k in range(self.output_size))
                delta_hidden[n][j] = error_hidden[n][j] * self.tanh_derivative(self.z1[n][j])

        for i in range(self.input_size):
            for j in range(self.hidden_size):
                grad = sum(X[n][i] * delta_hidden[n][j] for n in range(X.shape[0]))
                self.W1[i][j] -= self.learning_rate * grad / X.shape[0]

        for j in range(self.hidden_size):
            grad = sum(delta_hidden[n][j] for n in range(X.shape[0]))
            self.b1[0][j] -= self.learning_rate * grad / X.shape[0]

        for j in range(self.hidden_size):
            for k in range(self.output_size):
                grad = sum(self.a1[n][j] * delta_output[n][k] for n in range(X.shape[0]))
                self.W2[j][k] -= self.learning_rate * grad / X.shape[0]

        for k in range(self.output_size):
            grad = sum(delta_output[n][k] for n in range(X.shape[0]))
            self.b2[0][k] -= self.learning_rate * grad / X.shape[0]

        return np.mean(np.square(error_output))

    def train(self, X, Y, epochs=1000, print_every=100, print=False):
        for epoch in range(epochs):
            loss = self.train_step(X, Y)
            if (epoch % print_every == 0) and print:
                print(f"Epoch {epoch}: Loss = {loss:.6f}")

    def summary(self):
        print("Red neuronal inicializada:")
        print(f"W2 shape: {self.W2}, b2 shape: {self.b2}")
        print(f"W1 shape: {self.W1}, b1 shape: {self.b1}")
