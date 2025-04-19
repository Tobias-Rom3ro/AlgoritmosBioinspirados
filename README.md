# Algoritmos Bioinspirados para el Problema de la Mochila 🧬
Este proyecto implementa dos algoritmos bioinspirados para resolver el problema de la mochila con múltiples instancias de objetos:
1. **Enfriamiento Simulado (Simulated Annealing - SA)**
2. **Algoritmo de Colonia de Hormigas (Ant Colony Optimization - ACO)**

## Problema de la Mochila 🎒
El problema consiste en seleccionar la cantidad óptima de cada tipo de objeto para maximizar el valor total sin exceder la capacidad máxima de la mochila, considerando que puede haber múltiples unidades disponibles de cada objeto.
## Requisitos
- Python 3.7+
- Dependencias listadas en `requirements.txt`

Para instalar las dependencias ejecuta este comando: en la terminal:
``` bash
pip install -r requirements.txt
```
## Estructura del Proyecto 📂
- : Script principal que coordina la ejecución de los algoritmos `main.py`
- : Módulo para cargar datos desde archivo Excel `excel_reader.py`
- : Implementación del algoritmo de enfriamiento simulado `SimulatedAnnealing.py`
- : Implementación del algoritmo de colonia de hormigas `AntColony.py`

## Uso 💻
1. Coloque su archivo Excel con los datos de la mochila en el directorio del proyecto. El archivo debe llamarse preferentemente con el formato `Mochila_capacidad_maxima_XXkg.xlsx` donde XX es la capacidad máxima en kg.
2. Ejecute el programa principal:
``` bash
python main.py
```
1. Siga las instrucciones en pantalla para:
    - Seleccionar el algoritmo a ejecutar (SA, ACO o ambos)
    - Visualizar los resultados
    - Ejecutar múltiples veces para obtener estadísticas

## Formato del Archivo Excel 🧾
El archivo Excel debe contener las siguientes columnas:
- Peso_kg: Peso de cada objeto en kilogramos
- Valor: Valor o beneficio de cada objeto
- Cantidad: Cantidad máxima disponible de cada tipo de objeto

El programa intenta detectar automáticamente estas columnas o solicitará los nombres correctos si no puede hacerlo.
## Funcionamiento de los Algoritmos 🧑‍💻
### Enfriamiento Simulado (SA) 🥶
- Comienza con una solución aleatoria y la mejora progresivamente
- Permite movimientos que empeoran la solución con cierta probabilidad para escapar de óptimos locales
- La temperatura disminuye gradualmente, reduciendo la probabilidad de aceptar soluciones peores

### Colonia de Hormigas (ACO) 🐜
- Utiliza múltiples agentes (hormigas) que construyen soluciones
- Usa un modelo de feromonas para aprender de las mejores soluciones encontradas
- Combina exploración y explotación para encontrar soluciones óptimas

## Resultados 📒
Los algoritmos generan:
- Gráficos de convergencia (guardados como imágenes PNG)
- Detalles de la mejor solución encontrada
- Estadísticas de rendimiento cuando se ejecutan múltiples veces

## Parámetros Configurables 🧮
### Enfriamiento Simulado
- Temperatura inicial
- Temperatura final
- Tasa de enfriamiento

### Colonia de Hormigas
- Número de hormigas
- Número de iteraciones
- Parámetros alpha (importancia de feromonas) y beta (importancia de heurística)
- Tasa de evaporación de feromonas


## Interpretación de Resultados 🧠
- **Mejor valor**: El valor total máximo obtenido
- **Convergencia**: Iteración en la que se encontró la mejor solución
- **Tiempo de ejecución**: Tiempo total requerido para completar la búsqueda
- **Gráfico de convergencia**: Muestra cómo evoluciona el valor de la solución a lo largo de las iteraciones
