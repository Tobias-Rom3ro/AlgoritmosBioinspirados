import numpy as np
import matplotlib.pyplot as plt
import random
import time
import statistics

class KnapsackAntColony:
    def __init__(self, ant_count=50, max_iterations=200, alpha=1.0, beta=2.0, evaporation_rate=0.5, q=100):
        """
        Inicializa el algoritmo de colonias de hormigas.
        """
        self.ant_count = ant_count
        self.max_iterations = max_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.q = q

        # Datos del problema
        self.weights = []
        self.values = []
        self.quantities = []
        self.max_weight = 0
        self.n_items = 0

        # Feromonas e información heurística
        self.pheromone = None
        self.heuristic = None

        # Seguimiento
        self.iterations = 0
        self.convergence_iter = 0
        self.best_solution = None
        self.best_value = 0
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
        self.n_items = data["n_items"]

        # Inicializa feromonas e heurística
        max_q = [q + 1 for q in self.quantities]
        self.pheromone = [np.ones(mq) * 0.1 for mq in max_q]

        self.heuristic = []
        for i in range(self.n_items):
            item_h = []
            for k in range(self.quantities[i] + 1):
                item_h.append((k * self.values[i]) / (k * self.weights[i]) if k > 0 else 0.01)
            self.heuristic.append(item_h)

        return True

    def generate_ant_solution(self, iteration):
        """
        Genera una solución para una hormiga con exploración/explotación dinámica.
        """
        # Calcula factor de exploración: alto al inicio, bajo al final
        exploration = 1 - (iteration / self.max_iterations)
        dynamic_alpha = self.alpha * (1 - 0.5 * exploration)
        dynamic_beta = self.beta * (1 + 0.3 * exploration)

        solution = [0] * self.n_items
        remaining = self.max_weight
        order = list(range(self.n_items))
        random.shuffle(order)

        for i in order:
            max_qty = min(self.quantities[i], int(remaining / self.weights[i]))
            if max_qty <= 0:
                continue

            probs = []
            total = 0
            for k in range(max_qty + 1):
                p = (self.pheromone[i][k] ** dynamic_alpha) * (self.heuristic[i][k] ** dynamic_beta)
                probs.append(p)
                total += p

            if total > 0:
                probs = [p / total for p in probs]
            else:
                probs = [1.0 / (max_qty + 1)] * (max_qty + 1)

            r = random.random()
            acc = 0
            for k, p in enumerate(probs):
                acc += p
                if acc >= r:
                    solution[i] = k
                    break

            remaining -= solution[i] * self.weights[i]

        return solution

    def calculate_value(self, sol):
        return sum(sol[i] * self.values[i] for i in range(self.n_items))

    def calculate_weight(self, sol):
        return sum(sol[i] * self.weights[i] for i in range(self.n_items))

    def update_pheromones(self, ants, vals):
        # Evaporación
        for i in range(self.n_items):
            for k in range(len(self.pheromone[i])):
                self.pheromone[i][k] *= (1 - self.evaporation_rate)

        # Deposita feromonas ponderado por rango
        ranked = sorted(zip(ants, vals), key=lambda x: -x[1])
        for rank, (sol, val) in enumerate(ranked, start=1):
            if val <= 0:
                continue
            delta = self.q / (val * rank)
            for i in range(self.n_items):
                self.pheromone[i][sol[i]] += delta

        # Control de límites de feromonas
        for i in range(self.n_items):
            max_p = max(self.pheromone[i])
            min_p = max_p * 0.01
            self.pheromone[i] = [min(max(min_p, p), max_p) for p in self.pheromone[i]]

    def run(self):
        """Ejecuta la colonia de hormigas reiniciando estado internamente."""
        start = time.time()
        # Reiniciar historial y mejor solución
        self.fitness_history = []
        self.convergence_iter = 0
        self.best_solution = None
        self.best_value = 0

        # Copia inicial de feromonas para reset
        pheromone_init = [p.copy() for p in self.pheromone]

        for it in range(self.max_iterations):
            ants, vals = [], []
            for _ in range(self.ant_count):
                sol = self.generate_ant_solution(it)
                w = self.calculate_weight(sol)
                if w <= self.max_weight:
                    v = self.calculate_value(sol)
                    ants.append(sol)
                    vals.append(v)
                    if v > self.best_value:
                        self.best_value = v
                        self.best_solution = sol.copy()
                        self.convergence_iter = it

            if ants:
                self.update_pheromones(ants, vals)

            self.fitness_history.append(self.best_value)

        self.iterations = self.max_iterations
        self.time_elapsed = time.time() - start
        # Restaurar feromonas originales para futuras ejecuciones
        self.pheromone = pheromone_init
        return self.best_solution, self.best_value, self.convergence_iter, self.time_elapsed

    def print_results(self):
        print("\n--- Resultados Colonia de Hormigas ---")
        print(f"Tiempo: {self.time_elapsed:.4f}s | Iteraciones: {self.iterations} | Convergencia: {self.convergence_iter}")
        print(f"Mejor valor: {self.best_value} | Peso: {self.calculate_weight(self.best_solution)}")
        print("Solución:")
        for i, q in enumerate(self.best_solution):
            if q > 0:
                print(f"  Ítem {i+1}: {q} unidades (valor {q*self.values[i]}, peso {q*self.weights[i]})")

    def plot_convergence(self):
        plt.figure(figsize=(10,6))
        plt.plot(self.fitness_history, 'r-')
        plt.title('Convergencia Colonia de Hormigas')
        plt.xlabel('Iteración')
        plt.ylabel('Valor mochila')
        plt.grid(True)
        plt.savefig('convergencia_aco.png')
        plt.show()