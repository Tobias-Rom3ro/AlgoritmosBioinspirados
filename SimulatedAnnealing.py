import matplotlib.pyplot as plt
import time
import random
import math
import statistics

class KnapsackSimulatedAnnealing:
    def __init__(self, initial_temp=1000, final_temp=1, cooling_rate=0.95, max_iterations=1000):
        """
        Inicializa el algoritmo de enfriamiento simulado.
        """
        self.initial_temp = initial_temp
        self.temp = initial_temp
        self.final_temp = final_temp
        self.cooling_rate = cooling_rate
        self.max_iterations = max_iterations

        # Datos del problema
        self.weights = []
        self.values = []
        self.quantities = []
        self.max_weight = 0

        # Soluciones
        self.current_solution = []
        self.best_solution = []
        self.current_value = 0
        self.best_value = 0
        self.current_weight = 0

        # Seguimiento
        self.iterations = 0
        self.convergence_iter = 0
        self.fitness_history = []
        self.time_elapsed = 0

    def set_problem_data(self, data):
        """
        Establece los datos del problema desde un diccionario.
        """
        self.weights = data["weights"]
        self.values = data["values"]
        self.quantities = data["quantities"]
        self.max_weight = data["max_weight"]
        return True

    def generate_initial_solution(self):
        n = len(self.weights)
        solution = [0] * n
        total_weight = 0
        for i in range(n):
            max_possible = min(self.quantities[i], int((self.max_weight - total_weight) / self.weights[i]))
            if max_possible > 0:
                solution[i] = random.randint(0, max_possible)
                total_weight += solution[i] * self.weights[i]
        self.current_solution = solution
        self.best_solution = solution.copy()
        self.current_weight = self.calculate_weight(solution)
        self.current_value = self.calculate_value(solution)
        self.best_value = self.current_value
        return solution

    def calculate_weight(self, solution):
        return sum(solution[i] * self.weights[i] for i in range(len(solution)))

    def calculate_value(self, solution):
        return sum(solution[i] * self.values[i] for i in range(len(solution)))

    def is_valid_solution(self, solution):
        if self.calculate_weight(solution) > self.max_weight:
            return False
        for i in range(len(solution)):
            if solution[i] < 0 or solution[i] > self.quantities[i]:
                return False
        return True

    def generate_neighbor(self, solution):
        n = len(solution)
        neighbor = solution.copy()
        idx = random.randint(0, n-1)
        change = random.choice([-1, 1])
        if change == -1 and neighbor[idx] == 0:
            change = 1
        if change == 1 and neighbor[idx] >= self.quantities[idx]:
            change = -1
        neighbor[idx] += change
        if not self.is_valid_solution(neighbor):
            while self.calculate_weight(neighbor) > self.max_weight:
                remove_idx = random.randint(0, n-1)
                if neighbor[remove_idx] > 0:
                    neighbor[remove_idx] -= 1
        return neighbor

    def accept_probability(self, current_value, new_value, temperature):
        if new_value > current_value:
            return 1.0
        return math.exp((new_value - current_value) / temperature)

    def run(self):
        start_time = time.time()
        self.generate_initial_solution()
        self.temp = self.initial_temp
        self.fitness_history = [self.current_value]
        iteration = 0
        iterations_without_improvement = 0
        self.convergence_iter = 0
        while self.temp > self.final_temp and iteration < self.max_iterations:
            neighbor = self.generate_neighbor(self.current_solution)
            neighbor_value = self.calculate_value(neighbor)
            prob = self.accept_probability(self.current_value, neighbor_value, self.temp)
            if random.random() < prob:
                self.current_solution = neighbor
                self.current_value = neighbor_value
                self.current_weight = self.calculate_weight(neighbor)
                if self.current_value > self.best_value:
                    self.best_solution = self.current_solution.copy()
                    self.best_value = self.current_value
                    self.convergence_iter = iteration
                    iterations_without_improvement = 0
                else:
                    iterations_without_improvement += 1
            else:
                iterations_without_improvement += 1
            self.temp *= self.cooling_rate
            self.fitness_history.append(self.best_value)
            iteration += 1
            if iterations_without_improvement > 100:
                self.temp = self.initial_temp * 0.5
                iterations_without_improvement = 0
        self.iterations = iteration
        self.time_elapsed = time.time() - start_time
        return self.best_solution, self.best_value, self.convergence_iter, self.time_elapsed

    def print_results(self):
        print("\n--- Resultados del Enfriamiento Simulado ---")
        print(f"Tiempo de ejecución: {self.time_elapsed:.4f} segundos")
        print(f"Iteraciones totales: {self.iterations}")
        print(f"Iteración de convergencia: {self.convergence_iter}")
        print(f"Mejor valor encontrado: {self.best_value}")
        print(f"Peso total de la mejor solución: {self.calculate_weight(self.best_solution)}")
        print("Objetos seleccionados:")
        for i, q in enumerate(self.best_solution):
            if q > 0:
                print(f"Objeto {i+1}: {q} unidades, Valor: {q*self.values[i]}, Peso: {q*self.weights[i]}")

    def plot_convergence(self):
        plt.figure(figsize=(10, 6))
        plt.plot(range(len(self.fitness_history)), self.fitness_history, 'b-')
        plt.title('Convergencia de Enfriamiento Simulado')
        plt.xlabel('Iteraciones')
        plt.ylabel('Valor de la mochila')
        plt.grid(True)
        plt.savefig('convergencia_sa.png')
        plt.show()