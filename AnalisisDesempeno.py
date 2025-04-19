import matplotlib.pyplot as plt
import numpy as np
import statistics

def ejecutar_varias_veces_sa(sa, n=30):
    """Ejecuta el algoritmo de enfriamiento simulado varias veces y muestra estadísticas con gráfico."""
    valores = []
    tiempos = []
    iteraciones = []

    print(f"Ejecutando SA {n} veces...")
    for i in range(n):
        if i % 5 == 0:
            print(f"Progreso: {i}/{n}")
        sa.generate_initial_solution()
        _, valor, iter_conv, tiempo = sa.run()
        valores.append(valor)
        tiempos.append(tiempo)
        iteraciones.append(iter_conv)

    # Cálculo de estadísticas
    promedio = statistics.mean(valores)
    minimo = min(valores)
    maximo = max(valores)
    varianza = statistics.variance(valores)

    # Crear figura con dos subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Gráfico de convergencia de la última ejecución
    ax1.plot(sa.fitness_history, 'b-')
    ax1.set_title('Convergencia de Enfriamiento Simulado')
    ax1.set_xlabel('Iteración')
    ax1.set_ylabel('Valor de la mochila')
    ax1.grid(True)

    # Gráfico de barras para todas las ejecuciones
    x = np.arange(len(valores))
    ax2.bar(x, valores, color='blue', alpha=0.7)
    ax2.axhline(y=promedio, color='r', linestyle='-', label=f'Promedio: {promedio:.2f}')
    ax2.set_title(f'Desempeño en {n} ejecuciones')
    ax2.set_xlabel('Ejecuciones')
    ax2.set_ylabel('Costo Total')
    ax2.legend()
    ax2.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig(f'desempeno_sa_{n}_ejecuciones.png')
    plt.show()

    # Resumen estadístico
    print("\n--- Estadísticas después de varias ejecuciones SA ---")
    print(f"Resumen de las {n} ejecuciones:")
    print(f"Promedio valor óptimo: {promedio:.2f}")
    print(f"Mínimo: {minimo:.2f}")
    print(f"Máximo: {maximo:.2f}")
    print(f"Varianza: {varianza:.2f}")
    print(f"Promedio tiempo (s): {statistics.mean(tiempos):.4f} ± {statistics.stdev(tiempos):.4f}")
    print(
        f"Promedio iteraciones de convergencia: {statistics.mean(iteraciones):.2f} ± {statistics.stdev(iteraciones):.2f}")

    return valores, tiempos, iteraciones


def ejecutar_varias_veces_aco(aco, n=30):
    """Ejecuta el algoritmo de colonia de hormigas varias veces y muestra estadísticas con gráfico."""
    vals = []
    times = []
    iters = []

    print(f"Ejecutando ACO {n} veces...")
    for i in range(n):
        if i % 5 == 0:
            print(f"Progreso: {i}/{n}")
        _, v, itc, t = aco.run()
        vals.append(v)
        times.append(t)
        iters.append(itc)

    # Cálculo de estadísticas
    promedio = statistics.mean(vals)
    minimo = min(vals)
    maximo = max(vals)
    varianza = statistics.variance(vals)

    # Crear figura con dos subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Gráfico de convergencia de la última ejecución
    ax1.plot(aco.fitness_history, 'r-')
    ax1.set_title('Convergencia Colonia de Hormigas')
    ax1.set_xlabel('Iteración')
    ax1.set_ylabel('Valor mochila')
    ax1.grid(True)

    # Gráfico de barras para todas las ejecuciones
    x = np.arange(len(vals))
    ax2.bar(x, vals, color='blue', alpha=0.7)
    ax2.axhline(y=promedio, color='r', linestyle='-', label=f'Promedio: {promedio:.2f}')
    ax2.set_title(f'Desempeño en {n} ejecuciones')
    ax2.set_xlabel('Ejecuciones')
    ax2.set_ylabel('Costo Total')
    ax2.legend()
    ax2.grid(True, axis='y')

    plt.tight_layout()
    plt.savefig(f'desempeno_aco_{n}_ejecuciones.png')
    plt.show()

    # Mostrar resumen estadístico
    print("\n--- Estadísticas después de varias ejecuciones ACO ---")
    print(f"Resumen de las {n} ejecuciones:")
    print(f"Valor promedio: {promedio:.2f}")
    print(f"Valor mínimo: {minimo:.2f}")
    print(f"Valor máximo: {maximo:.2f}")
    print(f"Varianza: {varianza:.2f}")
    print(f"Tiempo promedio: {statistics.mean(times):.4f}s ± {statistics.stdev(times):.4f}s")
    print(f"Iter. convergencia: {statistics.mean(iters):.2f} ± {statistics.stdev(iters):.2f}")

    return vals, times, iters