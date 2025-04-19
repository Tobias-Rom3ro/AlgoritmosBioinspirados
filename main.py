import os
import statistics
from excel_reader import find_excel, load_data
from SimulatedAnnealing import KnapsackSimulatedAnnealing
from AntColony import KnapsackAntColony

def main():
    # Buscar archivo Excel
    try:
        path = find_excel()
        print(f"Usando archivo: {os.path.basename(path)}")
    except FileNotFoundError as e:
        path = input(str(e) + " Ruta del Excel: ")
        if not path:
            print("Cancelado. No hay archivo.")
            return

    # Cargar datos
    data = load_data(path)
    if not data:
        print("Error al cargar los datos. Terminando ejecución.")
        return

    # Menú para elegir el algoritmo
    print("\n--- Seleccione el algoritmo a ejecutar ---")
    print("1. Enfriamiento Simulado (SA)")
    print("2. Colonia de Hormigas (ACO)")
    print("3. Ambos algoritmos")
    
    opcion = input("Ingrese su opción (1-3): ")
    
    if opcion in ['1', '3']:
        print("\nEjecutando Enfriamiento Simulado...")
        sa = KnapsackSimulatedAnnealing(
            initial_temp=1000,
            final_temp=1,
            cooling_rate=0.95,
            max_iterations=1000
        )
        sa.set_problem_data(data)
        sa.run()
        sa.print_results()
        sa.plot_convergence()
        
        ejecutar_multiple = input("\n¿Desea ejecutar múltiples veces para obtener estadísticas? (s/n): ")
        if ejecutar_multiple.lower() == 's':
            veces = int(input("Número de ejecuciones: "))
            ejecutar_varias_veces_sa(sa, veces)
    
    if opcion in ['2', '3']:
        print("\nEjecutando Colonia de Hormigas...")
        aco = KnapsackAntColony(
            ant_count=50,
            max_iterations=200,
            alpha=1.0,
            beta=2.0,
            evaporation_rate=0.5,
            q=100
        )
        aco.set_problem_data(data)
        aco.run()
        aco.print_results()
        aco.plot_convergence()
        
        ejecutar_multiple = input("\n¿Desea ejecutar múltiples veces para obtener estadísticas? (s/n): ")
        if ejecutar_multiple.lower() == 's':
            veces = int(input("Número de ejecuciones: "))
            ejecutar_varias_veces_aco(aco, veces)

def ejecutar_varias_veces_sa(sa, n=30):
    """Ejecuta el algoritmo de enfriamiento simulado varias veces y muestra estadísticas."""
    valores = []
    tiempos = []
    iteraciones = []

    for _ in range(n):
        sa.generate_initial_solution()
        _, valor, iter_conv, tiempo = sa.run()
        valores.append(valor)
        tiempos.append(tiempo)
        iteraciones.append(iter_conv)

    print("\n--- Estadísticas después de varias ejecuciones SA ---")
    print(f"Promedio valor óptimo: {statistics.mean(valores):.2f} ± {statistics.stdev(valores):.2f}")
    print(f"Promedio tiempo (s): {statistics.mean(tiempos):.4f} ± {statistics.stdev(tiempos):.4f}")
    print(f"Promedio iteraciones de convergencia: {statistics.mean(iteraciones):.2f} ± {statistics.stdev(iteraciones):.2f}")

def ejecutar_varias_veces_aco(aco, n=30):
    """Ejecuta el algoritmo de colonia de hormigas varias veces y muestra estadísticas."""
    vals, times, iters = [], [], []
    for _ in range(n):
        _, v, itc, t = aco.run()
        vals.append(v)
        times.append(t)
        iters.append(itc)
    print("\n--- Estadísticas después de varias ejecuciones ACO ---")
    print(f"Valor promedio: {statistics.mean(vals):.2f} ± {statistics.stdev(vals):.2f}")
    print(f"Tiempo promedio: {statistics.mean(times):.4f}s ± {statistics.stdev(times):.4f}s")
    print(f"Iter. convergencia: {statistics.mean(iters):.2f} ± {statistics.stdev(iters):.2f}")

if __name__ == "__main__":
    main()